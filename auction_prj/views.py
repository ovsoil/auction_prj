from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator


class IndexView(TemplateView):
    template_name = 'index.html'

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)


class AngularView(TemplateView):
    def get_template_names(self):
        self.template_name = 'auction-gallery/auction-gallery.html'
        template_name = self.kwargs.get('template_name')
        folder = self.kwargs.get('folder')
        if template_name is None:
            return
        if folder is None:
            folder = ''
        if template_name[-1] == '/':
            self.template_name = '%s%s.html' % (folder, template_name[:-1])
        else:
            self.template_name = '%s%s.html' % (folder, template_name)

    @method_decorator(ensure_csrf_cookie)
    def dispath(self, request, *args, **kwargs):
        return super(AngularView, self).dispath(request, *args, **kwargs)

