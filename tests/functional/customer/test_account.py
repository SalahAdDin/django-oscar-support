from django.core.urlresolvers import reverse

from oscar_testsupport.testcases import WebTestCase
from oscar_testsupport.factories import create_order

from oscar_support.models import Ticket, TicketStatus, TicketType


class TestACustomer(WebTestCase):
    is_anonymous = False

    def setUp(self):
        super(TestACustomer, self).setUp()
        self.status = TicketStatus.objects.create(name="New")
        self.type = TicketType.objects.create(name="Question")

        self.subject = "this is the subject line"
        self.message_text = "this is a new message text"

    def test_can_create_a_new_ticket(self):
        page = self.get(reverse('support:customer-ticket-create'))

        ticket_form = page.forms['create-ticket-form']
        ticket_form['type'] = self.type.id
        ticket_form['subject'] = self.subject
        ticket_form['body'] = self.message_text
        page = ticket_form.submit()

        user_tickets = Ticket.objects.filter(requester=self.user)
        self.assertEquals(user_tickets.count(), 1)

        ticket = user_tickets[0]
        self.assertEquals(ticket.status, self.status)
        self.assertEquals(ticket.type, self.type)
        self.assertEquals(ticket.subject, self.subject)
        self.assertEquals(ticket.body, self.message_text)
        self.assertEquals(ticket.number, '1')
        self.assertEquals(ticket.subticket_number, 0)
        self.assertEquals(ticket.relatedorders.count(), 0)

    def test_can_create_a_ticket_with_related_order(self):
        order = create_order(user=self.user)
        page = self.get(reverse('support:customer-ticket-create'))

        ticket_form = page.forms['create-ticket-form']
        ticket_form['type'] = self.type.id
        ticket_form['subject'] = self.subject
        ticket_form['body'] = self.message_text
        ticket_form['order'] = order.id
        page = ticket_form.submit()

        user_tickets = Ticket.objects.filter(requester=self.user)
        self.assertEquals(user_tickets.count(), 1)

        ticket = user_tickets[0]
        self.assertEquals(ticket.status, self.status)
        self.assertEquals(ticket.type, self.type)
        self.assertEquals(ticket.subject, self.subject)
        self.assertEquals(ticket.body, self.message_text)
        self.assertEquals(ticket.number, '1')
        self.assertEquals(ticket.subticket_number, 0)

        self.assertEquals(ticket.relatedorders.count(), 1)
        self.assertEquals(ticket.relatedorders.all()[0].order.id, order.id)

    def test_can_add_message_to_a_ticket(self):
        ticket = Ticket.objects.create(
            requester=self.user,
            status=self.status,
            type=self.type,
            subject='This is the subject line',
            body="I have a question about something",
        )
        self.assertEquals(ticket.messages.count(), 0)

        page = self.get(reverse('support:customer-ticket-update',
                                args=(ticket.id,)))
        self.assertContains(page, ticket.body)

        message_form = page.forms['add-message-form']
        message_form['message_text'] = 'this is some additional message'
        message_form.submit()

        ticket = Ticket.objects.get(id=ticket.id)
        self.assertEquals(ticket.messages.count(), 1)
