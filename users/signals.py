from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from allauth.socialaccount.models import SocialAccount
import media
import numpy as np
import urllib.request
import cv2
from PIL import Image as im
import os

# METHOD #1: OpenCV, NumPy, and urllib

def url_to_image(url, username):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    resp = urllib.request.urlopen(url)
    print("1")
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    print("2")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    print("3")
    # final_image = im.fromarray(image)
    path = "D:\OneDrive - IIT Delhi\Desktop\DevClub\AIITRA\AIITRA\media\profile_pics"
    final_path = os.path.join(path, f'{username}.jpg')
    cv2.imwrite(final_path, image)
    # return the image
    print(final_path)
    return final_path


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        # if SocialAccount.objects.filter(user=instance).exists():
        #     print("exists")
        #     current_user = SocialAccount.objects.filter(user=instance)[0]
        #     pp = current_user.extra_data['picture']
        # else:
        #     pp = 'default.png'
        # print("pp= " + pp)
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=SocialAccount)
def edit_profile(sender, instance, created, **kwargs):
    if created:
        p = Profile.objects.filter(user=instance.user)[0]
        p.delete()
        if instance.provider == "google":
            pp = instance.extra_data['picture']
        elif instance.provider == "github":
            pp = instance.extra_data["avatar_url"]
        Profile.objects.create(user=instance.user, image=url_to_image(pp, instance.user.username))

        # print("pp" + pp)


@receiver(post_save, sender=SocialAccount)
def save_profile(sender, instance, **kwargs):
    instance.user.profile.save()
    print(instance.user.profile.image)
# @receiver(post_save, sender=SocialAccount)
# def save_profile_edited(sender, instance, **kwargs):


        # if SocialAccount.objects.filter(user=instance.user).exists():
        #     print("exists")
        #     current_user = SocialAccount.objects.filter(user=instance.user)[0]
        #     pp = current_user.extra_data['picture']
        #
        # else:
        #     pp = 'default.jpg'

        # print("pp= " + pp)
        # p.image=pp
        # p.save()

#
# @receiver(post_save, sender=User)
# def save_profile_pic(sender, instance, **kwargs):
#     pp=User.objects.get(email=instance.email)
#     SocialUser = SocialAccount.objects.filter(user=instance).first()
#     if SocialUser is not None:
#         extradata = SocialUser.extra_data
#         pp.image = extradata["picture"]
#         pp.save()
