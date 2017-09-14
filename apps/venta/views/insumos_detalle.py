from django.core.urlresolvers import reverse_lazy, reverse
# from django.utils.decorators import method_decorator
# from django.utils.translation import ugettext as _  # , ungettext
from django.utils.text import capfirst  # , get_text_list
from django.contrib import messages
from django.views import generic
from django.http import HttpResponseRedirect  # , HttpResponse
# from django.conf import settings
# from django.core import serializers
from django.utils.encoding import force_text
# from backend_apps.utils.decorators import permission_resource_required
# from backend_apps.utils.forms import empty
from backend_apps.utils.security import get_dep_objects  # log_params, SecurityKey, UserToken
# from decimal import Decimal

from ..models.detalle import Detalle
from ..models.insumos_detalle import InsumosDetalle
from ..forms.insumos_detalle import InsumosDetalleForm


class InsumosDetalleCreateView(generic.CreateView):
    model = InsumosDetalle
    form_class = InsumosDetalleForm
    template_name = "menu/form.html"
    # template_name = "insumos_detalle/form.html"

    def get_success_url(self):
        return reverse('venta:detalle_list', kwargs={'menu': self.object.detalle.menu.pk})

    # def get_initial(self):
    #     initial = self.initial.copy()
    #     initial['detalle_id'] = self.kwargs['detalle']
    #     return initial

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.detalle = Detalle.objects.get(id=self.kwargs['detalle'])
        # Actualizando costo del detalle
        costo = 0
        for d in self.object.detalle.insumosdetalle_set.all():
            costo += d.insumo.costo * d.cantidad
        costo += self.object.insumo.costo * self.object.cantidad
        self.object.detalle.costo = costo
        self.object.detalle.save()
        # Actualizando stock de insumo
        self.object.insumo.stock -= self.object.cantidad
        self.object.insumo.save()
        msg = ('%(name)s "%(obj)s" fue agregado satisfactoriamente') % {
            'name': self.model._meta.verbose_name,
            'obj': self.object
        }
        messages.success(self.request, msg)
        return super(InsumosDetalleCreateView, self).form_valid(form)


class InsumosDetalleDeleteView(generic.DeleteView):
    model = InsumosDetalle
    success_url = reverse_lazy('venta:detalle_list')

    def delete(self, request, *args, **kwargs):
        try:
            d = self.get_object()
            self.success_url = reverse('venta:detalle_list', kwargs={'menu': d.detalle.menu.pk})
            deps, msg = get_dep_objects(d)
            # actualizando costo de detalle
            costo = d.insumo.costo * d.cantidad
            d.detalle.costo = d.detalle.costo - costo
            d.detalle.save()
            # actualizando stock de insumo
            d.insumo.stock += d.cantidad
            d.insumo.save()
            print(deps)
            if deps:
                messages.warning(
                    self.request,
                    ('No se puede eliminar %(name)s') %
                    {
                        "name": capfirst(force_text(
                            self.model._meta.verbose_name)
                        ) + '"' + force_text(d) + '"'
                    })
                raise Exception(msg)
            d.delete()
            msg = (' %(name)s "%(obj)s" fue eliminado satisfactoriamente.') % {
                'name': 'Insumo',
                # 'name': capfirst(force_text(self.model._meta.verbose_name)),
                'obj': force_text(d)
            }
            if not d.id:
                messages.success(self.request, msg)

        except Exception as e:
            messages.error(request, e)

        return HttpResponseRedirect(self.success_url)

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
