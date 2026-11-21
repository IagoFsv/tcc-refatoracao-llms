"""Rule of an approval workflow, built from the dicts of a web API response.

Public entry point: run(rule). Do not change its name or signature; the rest
of the file may be freely reorganized.
"""

from typing import Optional, List, Union, Any, Dict


class AAARuleActionResolution:
    value: Optional[str]

    def __init__(
        self,
        *,
        value: Optional[str] = None,
        **kwargs,
    ) -> None:
        if value is not None:
            self.value = value
        else:
            self.value = None


class AAARuleActionNotify:
    entity_type: Optional[str]

    def __init__(
        self,
        *,
        entity_type: Optional[str] = None,
        **kwargs,
    ) -> None:
        if entity_type is not None:
            self.entity_type = entity_type
        else:
            self.entity_type = None


class AAARuleAction:
    resolution: Optional[AAARuleActionResolution]
    notify: Optional[List[AAARuleActionNotify]]

    def __init__(
        self,
        *,
        resolution=None,
        notify=None,
        **kwargs,
    ) -> None:
        if resolution is None or isinstance(resolution, AAARuleActionResolution):
            self.resolution = resolution
        else:
            self.resolution = AAARuleActionResolution(**resolution)
        self.notify = []
        if notify is not None:
            for a in notify:
                if isinstance(a, dict):
                    self.notify.append(AAARuleActionNotify(**a))
                else:
                    self.notify.append(a)


class AAARuleConditionValue:
    field: Optional[str]
    values: Optional[List[str]]
    datatype: Optional[str]
    operator: Optional[str]

    def __init__(
        self,
        *,
        field: Optional[str] = None,
        values: Optional[List[str]] = None,
        datatype: Optional[str] = None,
        operator: Optional[str] = None,
        **kwargs,
    ) -> None:
        if field is not None:
            self.field = field
        else:
            self.field = None
        if values is not None:
            self.values = values
        else:
            self.values = None
        if datatype is not None:
            self.datatype = datatype
        else:
            self.datatype = None
        if operator is not None:
            self.operator = operator
        else:
            self.operator = None


class AAARuleCondition:
    datatype: Optional[str]
    operator: Optional[str]
    values: Optional[List[AAARuleConditionValue]]
    entity_type: Optional[str]

    def __init__(
        self,
        *,
        datatype: Optional[str] = None,
        operator: Optional[str] = None,
        values=None,
        entity_type: Optional[str] = None,
        **kwargs,
    ) -> None:
        if datatype is not None:
            self.datatype = datatype
        else:
            self.datatype = None
        if operator is not None:
            self.operator = operator
        else:
            self.operator = None
        self.values = []
        if values is not None:
            for a in values:
                if isinstance(a, dict):
                    self.values.append(AAARuleConditionValue(**a))
                else:
                    self.values.append(a)
        if entity_type is not None:
            self.entity_type = entity_type
        else:
            self.entity_type = None


class AAARule:
    id: Optional[str]
    team_id: Optional[str]
    title: Optional[str]
    action: Optional[AAARuleAction]
    condition: Optional[AAARuleCondition]
    def __init__(
        self,
        *,
        id: Optional[str] = None,
        team_id: Optional[str] = None,
        title: Optional[str] = None,
        action: Optional[Union[Dict[str, Any], AAARuleAction]] = None,
        condition: Optional[Union[Dict[str, Any], AAARuleCondition]] = None,
        **kwargs,
    ) -> None:
        if id is not None:
            self.id = id
        else:
            self.id = None
        if team_id is not None:
            self.team_id = team_id
        else:
            self.team_id = None
        if title is not None:
            self.title = title
        else:
            self.title = None
        self.action = action if action is None or isinstance(action, AAARuleAction) else AAARuleAction(**action)
        self.condition = (
            condition if condition is None or isinstance(condition, AAARuleCondition) else AAARuleCondition(**condition)
        )


def run(rule):
    """Builds a rule from the dict of the response, then a second rule that
    reuses the already built action and condition. Returns both. Public entry
    point of this unit."""
    first = AAARule(**rule)
    second = AAARule(id=first.id, action=first.action, condition=first.condition)
    return first, second
