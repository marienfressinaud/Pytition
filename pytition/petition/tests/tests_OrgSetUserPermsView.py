from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import constants

from .utils import add_default_data

from petition.models import PytitionUser, Permission, Organization


class OrgSetUserPermsViewTest(TestCase):
    """Test org_edit_user_perms view"""

    @classmethod
    def setUpTestData(cls):
        add_default_data()

    def login(self, name, password=None):
        self.client.login(username=name, password=password if password else name)
        self.pu = PytitionUser.objects.get(user__username=name)
        return self.pu

    def logout(self):
        self.client.logout()

    def test_OrgSetUserPermsViewGetRedirectOk(self):
        julia = self.login("julia")
        response = self.client.get(reverse("org_set_user_perms", kwargs={'orgslugname': 'rap', 'user_name': 'julia'}),
                                   follow=True)
        self.assertRedirects(response, reverse("org_edit_user_perms", kwargs={'orgslugname': 'rap', 'user_name': 'julia'}))

    def test_OrgSetUserPermsViewPostOk(self):
        julia = self.login("julia")
        # Let's give julia rights to modify perms
        julia_perms = Permission.objects.get(organization__slugname="rap", user=julia)
        julia_perms.can_add_members = True
        # Add permission to edit permissions
        julia_perms.can_modify_permissions = True
        julia_perms.save()
        data = {
            'can_remove_members': 'on',
        }
        self.assertEqual(julia_perms.can_remove_members, False)
        response = self.client.post(reverse("org_set_user_perms", kwargs={'orgslugname': 'rap', 'user_name': 'julia'}),
                                    data, follow=True)
        self.assertRedirects(response, reverse("org_edit_user_perms",
                                               kwargs={'orgslugname': 'rap', 'user_name': 'julia'}))
        julia_perms = Permission.objects.get(organization__slugname="rap", user=julia)
        self.assertEquals(julia_perms.can_remove_members, True)

    def test_OrgSetUserPermsViewLastAdminRemoveItsPermsKO(self):
        julia = self.login("julia")
        # Let's give julia rights to modify perms ("admin" rights)
        julia_perms = Permission.objects.get(organization__slugname="rap", user=julia)
        julia_perms.can_modify_permissions = True
        julia_perms.save()
        # Now let's try to remove those...
        # It should fail in order to make it impossible to have an admin-less Organization
        data = {
            'can_modify_permissions': 'off',
        }
        self.assertEqual(julia_perms.can_modify_permissions, True)
        response = self.client.post(reverse("org_set_user_perms", kwargs={'orgslugname': 'rap', 'user_name': 'julia'}),
                                    data, follow=True)
        self.assertRedirects(response, reverse("org_edit_user_perms",
                                               kwargs={'orgslugname': 'rap', 'user_name': 'julia'}))
        self.assertEqual(response.context['permissions'].can_modify_permissions, True)
        julia_perms = Permission.objects.get(organization__slugname="rap", user=julia)
        self.assertEquals(julia_perms.can_modify_permissions, True)
        messages = response.context['messages']
        self.assertGreaterEqual(len(messages), 1)
        ThereIsAnyError = False
        for msg in messages:
            if msg.level == constants.ERROR:
                ThereIsAnyError = True
        self.assertEquals(ThereIsAnyError, True)
