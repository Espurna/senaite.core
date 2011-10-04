## Script (Python) "guard_reinstate"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##

from bika.lims import CancelAndReinstate

wf_tool = context.portal_workflow
checkPermission = context.portal_membership.checkPermission

if context.portal_type == 'AnalysisRequest':
    sample = context.getSample()
    if wf_tool.getInfoFor(sample, 'cancellation_state') == "cancelled":
        return False
    for analysis in context.getAnalyses(full_objects = True):
        if not checkPermission(CancelAndReinstate, analysis):
            return False
    return True

elif context.portal_type == 'Sample':
    for ar in context.getAnalysisRequests():
        if not checkPermission(CancelAndReinstate, ar):
            return False
        for analysis in ar.getAnalyses(full_objects = True):
            if not checkPermission(CancelAndReinstate, ar):
                return False
    return True

return True
