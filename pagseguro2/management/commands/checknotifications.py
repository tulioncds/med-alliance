import traceback
import sys

from django.core.management.base import BaseCommand, CommandError

from pagseguro2.choices import CHECKED_NO
from pagseguro2.choices import CHECKED_YES_FAILURE
from pagseguro2.choices import CHECKED_YES_SUCCESS
from pagseguro2.models import Notification

class Command(BaseCommand):
    help = u"Consults all unchecked notifications registered in the system"
    
    def handle(self, *args, **options):
        checked_success = 0
        checked_failure = 0
        failure_codes = []
        
        queryset = Notification.objects.filter(checked=CHECKED_NO[0])
        total = len(queryset)
        
        if total == 0:
            print "There are no unchecked notifications."
            return
        
        try:
            for notification in queryset:
                try:
                    notification.check()
                    
                    if notification.checked == CHECKED_YES_SUCCESS[0]:
                        checked_success += 1
                    elif notification.checked == CHECKED_YES_FAILURE[0]:
                        checked_failure += 1
                        failure_codes.append(notification.code)
                except:
                    # in this case its still an unchecked notification and 
                    # there is nothing to do.
                    pass
                
                    
            print '''%d unchecked notifications checked.
%d of them still unchecked.
%d of them successfully checked and updated.
%d of them failed to check. You should try again another time.''' %(total, total - checked_success - checked_failure, checked_success, checked_failure)                     

            if failure_codes:
                print "\nThe codes of notifications checked and failed follow:"
                for code in failure_codes:
                    print code

        except Exception, e:
            traceback.print_exc(file=sys.stdout)
            raise CommandError(e)
