"""
API for the gating djangoapp
"""
from django.contrib.auth.models import User
from opaque_keys.edx.keys import UsageKey
from xmodule.modulestore.django import modulestore
from xmodule.util.xblock_traversal import get_xblock_parent
from milestones import api as milestones_api
from openedx.core.lib.gating import api as gating_api


@gating_api.milestones_active(default=False)
def evaluate_prerequisite(user_id, course, prereq_content_key):
    """
    Finds the parent subsection of the content in the course and evaluates
    any milestone relationships attached to that subsection. If the calculated
    grade of the prerequisite subsection meets the minimum score required by
    dependent subsections, the related milestone will be fulfilled for the user.

    Arguments:
        user_id (int): ID of User for which evaluation should occur
        course_key (str|CourseKey): The course key
        prereq_content_key (str|UsageKey): The prerequisite content usage key

    Returns:
        None
    """
    xblock = modulestore().get_item(UsageKey.from_string(prereq_content_key))
    sequential = get_xblock_parent(xblock, 'sequential')
    if sequential:
        prereq_milestone = gating_api.get_gating_milestone(
            course.id,
            sequential.location.for_branch(None),
            'fulfills'
        )
        if prereq_milestone:
            gated_content_milestones = {}
            for milestone in gating_api.find_gating_milestones(course.id, None, 'requires'):
                milestone_id = milestone['id']
                gated_content = gated_content_milestones.get(milestone_id)
                if not gated_content:
                    gated_content = []
                    gated_content_milestones[milestone_id] = gated_content
                gated_content.append(milestone)

            gated_content = gated_content_milestones.get(prereq_milestone['id'])
            if gated_content:
                from courseware.grades import get_module_score
                user = User.objects.get(id=user_id)
                score = get_module_score(user, course, sequential) * 100
                for milestone in gated_content:
                    # Default minimum grade to 0
                    min_grade = 0
                    requirements = milestone.get('requirements')
                    if requirements:
                        try:
                            min_grade = int(requirements.get('min_grade'))
                        except (ValueError, TypeError):
                            pass

                    if score >= min_grade:
                        milestones_api.add_user_milestone({'id': user_id}, prereq_milestone)
                    else:
                        milestones_api.remove_user_milestone({'id': user_id}, prereq_milestone)
