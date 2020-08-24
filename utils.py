from decimal import Decimal

from django.core.cache import cache

from quiz.models import UserQuiz


def calculate_perc(subtotal, total):
    """ Calculates the percentage between 2 given numbers. """
    if not total:
        return '0'

    rat = Decimal((subtotal / total) * 100).quantize(Decimal('.01'))
    return str(rat).rstrip('0').rstrip('.') if '.' in str(rat) else str(rat)


def get_quiz_executions(quiz_id):
    """
    In case the cached value has been deleted (not likely to happen) or the first time this method is called
    calculate the value from db.
    In any other case return the cached value.
    """
    total_runs = cache.get('qtr:%s' % quiz_id)
    if total_runs is None:
        total_runs = UserQuiz.objects.filter(
            quiz_id=quiz_id,
            completed_at__isnull=False
        ).count()
        cache.set('qtr:%s' % quiz_id, total_runs)

    successful_runs = cache.get('qsr:%s' % quiz_id)
    if successful_runs is None:
        successful_runs = UserQuiz.objects.filter(
            quiz_id=quiz_id,
            completed_at__isnull=False,
            correct_answers__gt=7
        ).count()

        cache.set('qsr:%s' % quiz_id, successful_runs)

    return successful_runs, total_runs


def set_quiz_success_rate(quiz_id, is_successful=False):
    """ Sets the new quiz success rate values (success, total). """
    # call this method in order to re-create the cached data if somehow they are gone.
    _, _ = get_quiz_executions(quiz_id)

    # lock the cache to avoid race conditions
    cache.set('qtr:%s:lock' % quiz_id, '1', 60)

    cache.incr('qtr:%s' % quiz_id)
    if is_successful:
        cache.incr('qsr:%s' % quiz_id)

    # release the lock
    cache.delete('qtr:%s:lock' % quiz_id)
