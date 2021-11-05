from django.db.models import Count
from django_q.tasks import schedule, Schedule

from providers.models import Provider
from providers.scrapers.base import TF, TM, CHILDREN, ADOLESCENTS, ADULTS
from services.models import Service, ServiceType, ServiceAgeGroup, ServiceOffering, ServiceTime
from transgenderwachttijd.logging import logger

from .scrapers import scrapers


def initialize_tasks():
    if not Schedule.objects.filter(name='scrape').first():
        schedule('providers.tasks.scrape', name='scrape', schedule_type=Schedule.CRON, cron='00 12 * * *')


def scrape():
    types = {
        TF: ServiceType.objects.get(name=TF),
        TM: ServiceType.objects.get(name=TM)
    }
    age_groups = {
        CHILDREN: ServiceAgeGroup.objects.get(name=CHILDREN),
        ADOLESCENTS: ServiceAgeGroup.objects.get(name=ADOLESCENTS),
        ADULTS: ServiceAgeGroup.objects.get(name=ADULTS)
    }

    for scraper in scrapers:
        try:
            # Lookup provider
            provider = Provider.objects.filter(slug=scraper.get_provider_handle()).first()
            if not provider:
                raise Exception(f'Unknown provider "{scraper.get_provider_handle()}"')

            # Scrape service times
            service_times = scraper.scrape()
            print(service_times)

            # Loop over scraped service times
            for time in service_times:
                # TOOD: handle service with "individual" service times
                if time['days'] is None:
                    continue

                # Look up service
                service_name = time['service']
                service = Service.objects.filter(name_en=service_name).first()
                if not service:
                    raise Exception(f'Unknown service "{service_name}"')

                # Look up service types and age groups
                service_types = {types[t] for t in time['types']}
                service_age_groups = {age_groups[a] for a in time['age_groups']}

                # Look up service offerings
                service_offerings = ServiceOffering.objects.filter(provider=provider, service=service).all()

                # Filter by service types
                for service_type in service_types:
                    service_offerings = [o for o in service_offerings if o.types.filter(id=service_type.id).exists()]

                # Filter by service age groups
                for service_age_group in service_age_groups:
                    service_offerings = [o for o in service_offerings if o.age_groups.filter(id=service_age_group.id).exists()]

                # Check if the service offering exists
                service_offering = service_offerings[0] if len(service_offerings) > 0 else None
                if not service_offering:
                    # Create service offering
                    service_offering = ServiceOffering(provider=provider, service=service)
                    service_offering.save()
                    service_offering.types.add(*service_types)
                    service_offering.age_groups.add(*service_age_groups)

                # Create service time
                service_time = ServiceTime(offering=service_offering, days=time['days'])
                service_time.save()
        except Exception as err:
            logger.error(f'Failed to scrape using scraper "{type(scraper).__name__}":')
            logger.exception(err)
