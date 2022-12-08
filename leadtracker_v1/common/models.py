"""Models commonly used in all apps."""
from rest_framework import fields
from rest_framework.exceptions import ValidationError

from django.db import models
from django.conf import settings

from .library import encode


class AbstractBaseModel(models.Model):
    """
    Abstract base model for tracking.

    Atribs:
        creator(obj): Creator of the object
        updater(obj): Updater of the object
        created_on(datetime): Added date of the object
        updated_on(datetime): Last updated date of the object
    """

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        default=None,
        null=True,
        blank=True,
        related_name="creator_%(class)s_objects",
        on_delete=models.SET_NULL,
    )
    updater = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        default=None,
        null=True,
        blank=True,
        related_name="updater_%(class)s_objects",
        on_delete=models.SET_NULL,
    )
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta class for the above model."""

        abstract = True
        ordering = ("-created_on",)

    @property
    def idencode(self):
        """To return encoded id."""
        return encode(self.id)


class Address(models.Model):
    """
    Abstract model to group fields related to address
    """

    house_name = models.CharField(max_length=100, default="", blank=True)
    street = models.CharField(max_length=500, default="", blank=True)
    city = models.CharField(max_length=500, default="", blank=True)
    sub_province = models.CharField(max_length=500, default="", blank=True)
    province = models.CharField(max_length=500, default="", blank=True)
    country = models.CharField(max_length=500, default="", blank=True)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    zipcode = models.CharField(max_length=50, default="", blank=True)

    class Meta:
        """Meta class for the above model."""

        abstract = True


class GraphModel(models.Model):
    """
    Abstract model for creating Directed Acyclic Graph.
    Useful for creating transaction graph

    """

    class Meta:
        ordering = ("-id",)
        abstract = True

    def __unicode__(self):
        return "%s" % self.pk

    def add_parent(self, ancestor):
        """Function to add a parent"""
        self.circular_checker(ancestor, self)
        self.parents.add(ancestor)
        self.save()

    def add_child(self, child):
        """Function to add a child"""
        child.add_parent(self)

    def remove_parent(self, ancestor):
        """Function to remove a parent"""
        self.parents.remove(ancestor)
        self.save()

    def remove_child(self, child):
        """Function to remove a child"""
        child.remove_parent(self)

    def get_descendants(self, include_self=False):
        """Gets all children and their children recursively"""
        descendants_set = self.children.all().order_by("-id").distinct("id")
        for child in self.children.all():
            grand_children = child.get_descendants()
            descendants_set |= grand_children
        if include_self:
            descendants_set |= (
                self.__class__.objects.filter(id=self.id).order_by("-id").distinct("id")
            )
        return descendants_set

    def get_ancestors(self, include_self=False):
        """Gets all parents and their parents recursively"""
        ancestors_set = self.parents.all().order_by("-id").distinct("id")
        for parent in self.parents.all():
            grand_parent = parent.get_ancestors()
            ancestors_set |= grand_parent
        if include_self:
            ancestors_set |= (
                self.__class__.objects.filter(id=self.id).order_by("-id").distinct("id")
            )
        return ancestors_set

    def get_leaf_nodes(self):
        """Gets the ending nodes"""
        leaf_nodes = self.__class__.objects.none()
        children = self.children.all().order_by("-id").distinct("id")
        if not children:
            return (
                self.__class__.objects.filter(id=self.id).order_by("-id").distinct("id")
            )
        for child in children:
            leaf_nodes |= child.get_leaf_nodes()
        return leaf_nodes

    def get_root_nodes(self):
        """Gets the starting nodes"""
        root_nodes = self.__class__.objects.none()
        parents = self.parents.all().order_by("-id").distinct("id")
        if not parents:
            return (
                self.__class__.objects.filter(id=self.id).order_by("-id").distinct("id")
            )
        for parent in parents:
            root_nodes |= parent.get_root_nodes()
        return root_nodes

    def is_island(self):
        """Check if node is separated from the rest of the graph"""
        return not bool(self.parents.all() or self.children.all())

    @staticmethod
    def circular_checker(parent, child):
        """
        Checks that the object is not an ancestor, avoid self links
        """
        if parent == child:
            raise ValidationError("Self links are not allowed.")
        if child in parent.get_ancestors():
            raise ValidationError("The object is an ancestor.")
