# This file is part of Bika LIMS
#
# Copyright 2011-2016 by it's authors.
# Some rights reserved. See LICENSE.txt, AUTHORS.txt.

## Script (Python) "guard_submit_transition"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##

workflow = context.portal_workflow

# Can't do anything to the object if it's cancelled
if workflow.getInfoFor(context, 'cancellation_state', 'active') == "cancelled":
    return False

if context.portal_type == "Analysis":
    from bika.lims.workflow.analysis.guards import submit
    return submit(context)

if context.portal_type == "AnalysisRequest":
    # Only transition to 'attachment_due' if all analyses are at least there.
    has_analyses = False
    for a in context.objectValues('Analysis'):
        has_analyses = True
        review_state = workflow.getInfoFor(a, 'review_state')
        if review_state in ('to_be_sampled', 'to_be_preserved',
                            'sample_due', 'sample_received',):
            return False
    return has_analyses

if context.portal_type == "Worksheet":

    if not context.getAnalyst():
        return False

    # Only transition to 'attachment_due' if all analyses are at least there.
    has_analyses = False
    workflow = context.portal_workflow
    for a in context.getAnalyses():
        has_analyses = True
        review_state = workflow.getInfoFor(a, 'review_state', '')
        if review_state in ('sample_received', 'assigned',):
            # Note: referenceanalyses and duplicateanalyses can still have review_state = "assigned".
            return False
    return has_analyses
