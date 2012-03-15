#!/usr/bin/env python
# Steve Phillips / elimisteve
# 2012.03.15

import sys

SUPPORTED_RELATIONSHIPS = ['m2m', 'many2many',
                           'fk', 'foreignkey']

usage = "%s m2m app_name parent_model_name pluralized child_model_name pluralized" % (sys.argv[0])

if len(sys.argv) < 2:
    print usage
    sys.exit(0)

if sys.argv[1].lower() not in SUPPORTED_RELATIONSHIPS:
    print "Only m2m currently supported"
    sys.exit(0)

APP_NAME, PARENT, PARENT_PLURAL, CHILD, CHILD_PLURAL = sys.argv[2:]

replacement_data = {'parent': PARENT, 'parent_plural': PARENT_PLURAL,
                    'Parent': PARENT.capitalize(),
                    'child': CHILD, 'CHILD_PLURAL': CHILD_PLURAL,
                    'Child': CHILD.capitalize(),
                    'app_name': APP_NAME, 
                    }


print """
@login_required
def create_%(child)s(request):
    if request.method == 'POST':
        form = %(Child)sForm(request.POST)
        if form.is_valid():
            %(child)s = form.save()
            %(parent)s = %(Parent)s.objects.get(user=request.user)
            if %(parent)s not in %(child)s.%(parent_plural)s.all():
                %(child)s.%(parent_plural)s.add(%(parent)s)

            messages.success(request, 'New %(Child)s Created')
            return HttpResponseRedirect('/dashboard/')
        else:
            for field in form:
                for error in field.errors:
                    pass #messages.error(request, error)
    else:
        form = %(Child)sForm()
    return render(request, '%(app_name)s/%(child)s_detail.html', {'form': form })


@login_required
def read_%(child)s(request, %(child)s_id):
    %(parent)s = %(Parent)s.objects.get(user=request.user)
    #%(child)s = %(Child)s.objects.filter(%(parent_plural)s__id=%(parent)s.id)[0]
    try:
        %(child)s = %(parent)s.%(CHILD_PLURAL)s.get(id=int(%(child)s_id))
    except %(Child)s.DoesNotExist:
        messages.error(request, 'No such %(child)s')
        return HttpResponseRedirect('/dashboard/')
    form = %(Child)sForm(instance=%(child)s)
    c = {'%(child)s': %(child)s, 'form': form}
    return render(request, '%(app_name)s/%(child)s_detail.html', c)


@login_required
def read_all_%(CHILD_PLURAL)s(request):
    %(parent)s = %(Parent)s.objects.get(user=request.user)
    %(CHILD_PLURAL)s = %(parent)s.%(CHILD_PLURAL)s.all()
    #form = %(Child)sForm(instance=%(child)s)
    c = {'%(CHILD_PLURAL)s': %(CHILD_PLURAL)s} #, 'forms': form}
    return render(request, '%(app_name)s/%(child)s_list.html', c)


@login_required
def update_%(child)s(request, %(child)s_id):
    %(parent)s = %(Parent)s.objects.get(user=request.user)
    %(child)s = get_object_or_404(%(parent)s.%(CHILD_PLURAL)s, id=%(child)s_id)

    if request.method == 'POST':
        form = %(Child)sForm(request.POST, instance=%(child)s)
        if form.is_valid():
            %(child)s = form.save()
            messages.success(request, u"%(Child)s Updated.")
            return redirect("parent_dashboard")
    else:
        form = %(Child)sForm(instance=%(child)s)
    return render(request, '%(app_name)s/%(child)s_detail.html', {'form': form})


@login_required
def delete_%(child)s(request, %(child)s_id):
    %(parent)s = %(Parent)s.objects.get(user=request.user)
    try:
        %(child)s = %(parent)s.%(CHILD_PLURAL)s.get(id=int(%(child)s_id))
    except:
        messages.error(request, 'No such %(child)s')
        return HttpResponseRedirect('/dashboard/')
    %(child)s.delete()
    messages.success(request, '%(Child)s Deleted')
    return HttpResponseRedirect('/dashboard/')

""" % replacement_data
