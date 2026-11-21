from typing import Optional, List, Union, Any, Dict


class AAARuleActionResolution:
    value: Optional[str]

    def __init__(
        self,
         *,
        value: Optional[str] = None,
         **kwargs,
    ) -> None:
        self.value = value


class AAARuleActionNotify:
    entity_type: Optional[str]

    def __init__(
        self,
         *,
        entity_type: Optional[str] = None,
         **kwargs,
    ) -> None:
        self.entity_type = entity_type


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
        self.resolution = resolution if resolution is None or isinstance(resolution, AAARuleActionResolution) else AAARuleActionResolution(**resolution)
        self.notify = [] if notify is not None else None
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
        self.field = field
        self.values = values
        self.datatype = datatype
        self.operator = operator


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
        self.datatype = datatype
        self.operator = operator
        self.values = [] if values is not None else None
        if values is not None:
            for a in values:
                if isinstance(a, dict):
                    self.values.append(AAARuleConditionValue(**a))
                else:
                    self.values.append(a)
        self.entity_type = entity_type


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
        self.id = id
        self.team_id = team_id
        self.title = title
        self.action = action if action is None or isinstance(action, AAARuleAction) else AAARuleAction(**action)
        self.condition = condition if condition is None or isinstance(condition, AAARuleCondition) else AAARuleCondition(**condition)


def run(rule):
    first = AAARule(**rule)
    second = AAARule(id=first.id, action=first.action, condition=first.condition)
    return first, second
