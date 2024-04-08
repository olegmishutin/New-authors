import os


def changeFile(oldFile, newFile=None, deleteOnly=False):
    if not newFile and not deleteOnly:
        return oldFile

    if oldFile and os.path.isfile(oldFile.path) and oldFile != newFile:
        os.remove(oldFile.path)
    return newFile


def filterContext(request, queryset, checkboxesFilters):
    filters, context = [], {}

    for checkbox, filter in checkboxesFilters.items():
        if request.GET.get(checkbox):
            filters.append(filter)
            context[checkbox] = 'checked'

    return {'queryset': queryset.order_by(*filters), 'context': context}
