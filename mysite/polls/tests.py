from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse
import datetime
from polls.models import Question
class QuestionMethodTests(TestCase):
	def test_was_published_recently_with_future_question(self):
		time=timezone.now()+datetime.timedelta(days=30)
		future_question=Question(pub_date=time)
		self.assertEqual(future_question.was_published_recently(),False)
	def test_was_published_recently_with_old_question(self):
		time=timezone.now()-datetime.timedelta(days=2)
		old_question=Question(pub_date=time)
		self.assertEqual(old_question.was_published_recently(),False)
	def test_was_published_recently_with_recent_question(self):
		time=timezone.now()-datetime.timedelta(hours=3)
		recent_question=Question(pub_date=time)
		self.assertEqual(recent_question.was_published_recently(),True)
def create_question(question_text,days):
	date=timezone.now()+datetime.timedelta(days=days)
	return Question.objects.create(question_text=question_text,pub_date=date)
class QuestionViewTests(TestCase):
	def test_index_view_with_no_questions(self):
		response=self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code,200)
		self.assertContains(response,"No Polls available.")
		self.assertQuerysetEqual(response.context['latest_question_list'],[])
	def test_index_view_with_a_past_question(self):
		create_question('Past Question',-30)
		response=self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: Past Question>'])
	def test_index_view_with_a_future_question(self):
		create_question('Future Question',30)
		response=self.client.get(reverse('polls:index'))
		self.assertContains(response,"No Polls available.")
		self.assertQuerysetEqual(response.context['latest_question_list'],[])
	def test_index_view_with_past_and_future_question(self):
		create_question('Future Question',30)	
		create_question('Past Question',-30)
		response=self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: Past Question>'])
	def test_index_view_with_two_past_questions(self):
		create_question('Past Question1',-30)
		create_question('Past Question2',-30)
		response=self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: Past Question1>', '<Question: Past Question2>'])
class QuestionIndexDetailTests(TestCase):
	def test_detail_view_with_a_future_question(self):
		ftr_ques=create_question('future_question',30)
		response=self.client.get(reverse('polls:detail', args=(ftr_ques.id,)))
		self.assertEqual(response.status_code,404)
	def test_detail_view_with_a_past_question(self):
		past_ques=create_question('past_question',-30)
		response=self.client.get(reverse('polls:detail', args=(past_ques.id,)))
		self.assertEqual(response.status_code,200)
		self.assertContains(response,past_ques.question_text)