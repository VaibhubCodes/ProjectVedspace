# colleges/admin_mixins.py

from django.http import JsonResponse
from django.contrib.admin.views.main import ChangeList
from django.core.exceptions import PermissionDenied

class AjaxSearchMixin:
    def changelist_view(self, request, extra_context=None):
        if 'ajax_search' in request.GET:
            search_term = request.GET.get('q', '')
            cl = ChangeList(request, self.model, self.list_display,
                            self.list_display_links, self.list_filter,
                            self.date_hierarchy, self.search_fields,
                            self.list_select_related, self.list_per_page,
                            self.list_max_show_all, self.list_editable, self)

            cl.queryset = cl.queryset.filter(name__icontains=search_term)[:10]  # customize this line as needed
            results = [{'id': obj.id, 'name': str(obj)} for obj in cl.queryset]
            return JsonResponse(results, safe=False)
        return super().changelist_view(request, extra_context)
