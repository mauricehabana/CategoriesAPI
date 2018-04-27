from __future__ import unicode_literals

from django.utils.translation import ugettext as _
from django.db import models
from collections import OrderedDict


class Category(models.Model):
    """This model represents to categories."""
    name = models.CharField(max_length=50, unique=True, help_text=_("name of category."))
    parent = models.ForeignKey('Category', on_delete=models.CASCADE, default=None, blank=True, null=True)

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def parents(self):
        _parents = []
        _curr = self.parent
        while _curr is not None:
            _parents.append(_curr)
            _curr = _curr.parent

        return _parents

    def children(self):
        return Category.objects.filter(parent_id=self.pk)

    def siblings(self):
        get = Category.objects.filter(parent_id=self.parent.pk)
        exclude = get.exclude(pk=self.id)
        return exclude

    def get_json(self):
        return OrderedDict([
            (
                "id", self.id
            ), (
                "name", self.name
            ), (
                "parents", (self.get_list(self.parents())),
            ), (
                "children", (self.get_list(self.children())),
            ), (
                "siblings", (self.get_list(self.siblings())),
            )
        ])

    def get_list(self, _list):
        return [OrderedDict([("id", item.id), ("name", item.name)]) for item in _list]

    @staticmethod
    def create_category(in_json, parent=None):
        try:
            cat = Category.objects.create(name=in_json['name'], parent_id=parent)
            if 'children' in in_json:
                for item in in_json['children']:
                    Category.create_category(item, cat.pk)
        except:
            pass
