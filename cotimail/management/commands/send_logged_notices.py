import logging, time

from django.core.management.base import BaseCommand
from django.conf import settings

from cotimail.lockfile import FileLock, AlreadyLocked, LockTimeout
from cotimail.models import EmailLog

LOCK_WAIT_TIMEOUT = getattr(settings, "COTIMAIL_LOCK_WAIT_TIMEOUT", -1)

class Command(BaseCommand):
	help = "Send logged notices."
	
	def handle(self, *args, **options):

		# File locking
		# We lock the file in case the next schedule task it called before the current one has completed.
		lock = FileLock("send_logged_mail")
	
		logging.debug("acquiring lock...")
		try:
			lock.acquire(LOCK_WAIT_TIMEOUT)
		except AlreadyLocked:
			logging.debug("lock already in place. quitting.")
			return
		except LockTimeout:
			logging.debug("waiting for the lock timed out. quitting.")
			return
		logging.debug("acquired.")
		
		# Stamp the start time to determine the query length in the end
		start_time = time.time()

		# Set the default counts
		sent, failed = 0, 0

		# Get all logs
		logs = EmailLog.objects.filter(status__in=['QUEUED', 'FAILED'])

		try:
			# Send the logged emails
			for log in logs:
				if log.send():
					sent += 1
				else:
					failed += 1 

		finally:
			logging.debug("releasing lock...")
			lock.release()
			logging.debug("released.")
		
		logging.info("")
		logging.info("%s sent; %s failed;" % (sent, failed))
		logging.info("done in %.2f seconds" % (time.time() - start_time))
