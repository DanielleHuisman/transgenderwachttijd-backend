from django.db.models import Count

from providers.models import Provider
from providers.scrapers.base import Scraper, TF, TM, CHILDREN, ADOLESCENTS, ADULTS
from providers.scrapers.devaart import ScraperDeVaart
from providers.scrapers.psytrans import ScraperPsyTrans
from providers.scrapers.radboudumc import ScraperRadboudumc
from providers.scrapers.stepwork import ScraperStepwork
from providers.scrapers.umcg import ScraperUMCG
from providers.scrapers.vumc import ScraperVUmc
from services.models import Service, ServiceType, ServiceAgeGroup, ServiceOffering, ServiceTime


def test(scraper_name: str):
    types = {
        TF: ServiceType.objects.get(name=TF),
        TM: ServiceType.objects.get(name=TM)
    }
    age_groups = {
        CHILDREN: ServiceAgeGroup.objects.get(name=CHILDREN),
        ADOLESCENTS: ServiceAgeGroup.objects.get(name=ADOLESCENTS),
        ADULTS: ServiceAgeGroup.objects.get(name=ADULTS)
    }

    scraper: Scraper

    if scraper_name == 'devaart':
        scraper = ScraperDeVaart()
    elif scraper_name == 'psytrans':
        scraper = ScraperPsyTrans()
    elif scraper_name == 'radboudumc':
        scraper = ScraperRadboudumc()
    elif scraper_name == 'stepwork':
        scraper = ScraperStepwork()
    elif scraper_name == 'umcg':
        scraper = ScraperUMCG()
    elif scraper_name == 'vumc':
        scraper = ScraperVUmc()
    else:
        raise Exception(f'Unknown scraper "{scraper_name}"')

    # Lookup provider
    provider = Provider.objects.filter(slug=scraper.get_provider_handle()).first()
    if not provider:
        raise Exception(f'Unknown provider "{scraper.get_provider_handle()}"')

    # Scrape service times
    service_times = scraper.scrape()
    print(service_times)

    # Loop over scraped service times
    for time in service_times:
        # Look up service
        service_name = time['service']
        service = Service.objects.filter(name_en=service_name).first()
        if not service:
            raise Exception(f'Unknown service "{service_name}"')

        # Look up service types and age groups
        service_types = {types[t] for t in time['types']}
        service_age_groups = {age_groups[a] for a in time['age_groups']}

        # Look up service offering
        service_offerings = ServiceOffering.objects.filter(provider=provider, service=service).all()

        for service_type in service_types:
            service_offerings = [o for o in service_offerings if o.types.filter(id=service_type.id).exists()]

        for service_age_group in service_age_groups:
            service_offerings = [o for o in service_offerings if o.age_groups.filter(id=service_age_group.id).exists()]

        service_offering = service_offerings[0] if len(service_offerings) > 0 else None

        # Check if the service offering exists
        if not service_offering:
            # Create service offering
            service_offering = ServiceOffering(provider=provider, service=service)
            service_offering.save()
            service_offering.types.add(*service_types)
            service_offering.age_groups.add(*service_age_groups)

        # Create service time
        service_time = ServiceTime(offering=service_offering, days=time['days'])
        service_time.save()


test('vumc')
