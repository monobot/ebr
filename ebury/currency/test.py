# from model_mommy import mommy
# from django.contrib.auth.models import User

# from django.test import TestCase

# from rest_framework.exceptions import NotAcceptable


# class SecretSantaTest(TestCase):
#     def setUp(self):
#         self.man_user = mommy.make(User)
#         self.secretsanta = mommy.make(
#             'secretsanta.SecretSanta',
#             name='hola',
#             owner=self.man_user
#         )
#         self.other_user = mommy.make('User', username='otheruser')

#         mommy.make(
#             'secretsanta.Santa',
#             secretsanta=self.secretsanta,
#             _quantity=20
#         )
#         mommy.make(
#             'Santa',
#             secretsanta=self.secretsanta,
#             name=self.other_user.username,
#             age=19
#         )

#     def test_asignSantas(self):
#         # we try to close a secretsnta with 0 santas
#         mess = 'only 0 members in the secret santa, won\'t be too funny'
#         with self.assertRaisesMessage(NotAcceptable, mess):
#             mommy.make(
#                 'secretsanta.SecretSanta',
#                 name='hola2',
#                 owner=self.man_user,
#                 closed=True
#             )

#         # even with 2 santas, an exception will be raised
#         mess = 'only 2 members in the secret santa, won\'t be too funny'
#         with self.assertRaisesMessage(NotAcceptable, mess):
#             secretsanta = mommy.make(
#                 'secretsanta.SecretSanta',
#                 name='hola3',
#                 owner=self.man_user,
#             )
#             mommy.make(
#                 'secretsanta.Santa',
#                 secretsanta=secretsanta,
#                 _quantity=2,
#             )
#             secretsanta.closed = True
#             secretsanta.save()

#         self.assertFalse(self.secretsanta.closed)

#         # when we close the secretsanta is when the matches are created
#         self.secretsanta.closed = True
#         self.secretsanta.save()
#         self.assertTrue(self.secretsanta.closed)

#         # we have to check that each santa has other one assigned (different)
#         # and that at the end all of them are asigned
#         first_list = []
#         second_list = []
#         for santa in self.secretsanta.santas:
#             first_list.append(santa.id)
#             second_list.append(santa.gifts_to.id)
#             self.assertTrue(santa.id != santa.gifts_to.id)

#         first_list = set(sorted(first_list))
#         second_list = set(sorted(second_list))

#         self.assertFalse(first_list - second_list)
