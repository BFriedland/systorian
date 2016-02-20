from django.db.models import Max

from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView

from metrics.models import Entry
from metrics.serializers import EntrySerializer


class EntryViewSet(ModelViewSet):
    """ ViewSet for the Entry class """

    queryset = Entry.objects.all()
    serializer_class = EntrySerializer


# Reference: http://www.django-rest-framework.org/api-guide/filtering/
class CurrentEntryView(ListAPIView):

    serializer_class = EntrySerializer

    def get_queryset(self):
        # The view with the highest ID is also the most recent (i.e., current) view.
        # This convoluted syntax allows me to return it alone in a queryset.
        return Entry.objects.filter(id=Entry.objects.aggregate(Max('id'))['id__max'])
        # This also returns the most recent one, but it isn't in a queryset:
        # return Entry.objects.first()


def timestring_to_top_format(timestring):
    ''' Example format, for dev purposes: Fri Jan 29 20:00:35 2016 '''

    DATE_MAP = {
        'Jan': '01',
        'Feb': '02',
        'Mar': '03',
        'Apr': '04',
        'May': '05',
        'Jun': '06',
        'Jul': '07',
        'Aug': '08',
        'Sep': '09',
        'Oct': '10',
        'Nov': '11',
        'Dec': '12'
    }

    time_parts = timestring.split()
    for index, each in enumerate(time_parts):
        if len(each) == 1:
            time_parts[index] = str.zfill(each, 2)
    date = [time_parts[1], time_parts[2], time_parts[4]]
    formatted_date = [date[2], DATE_MAP[date[0]], date[1]]
    joined_date = '/'.join(formatted_date)
    return joined_date


class SingleDayEntryView(ListAPIView):

    serializer_class = EntrySerializer

    def get_queryset(self):
        time_parts = [self.kwargs['year'], self.kwargs['month'], self.kwargs['day']]
        for index, each in enumerate(time_parts):
            if len(each) == 1:
                time_parts[index] = str.zfill(each, 2)
        joined_date = '/'.join(time_parts)

        return Entry.objects.filter(data__capture_time__date=joined_date)


