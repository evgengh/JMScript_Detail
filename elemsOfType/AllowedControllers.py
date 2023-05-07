from enum import Enum

class ControllerType(Enum):
    IfController ='IfController'
    TransactionController = 'TransactionController'
    ThroughputController = 'ThroughputController'
    GenericController = 'GenericController'
    OnceOnlyController = 'OnceOnlyController'
    LoopController = 'LoopController'
    WhileController = 'WhileController'
    CriticalSectionController = 'CriticalSectionController'
    ForeachController = 'ForeachController'
    IncludeController = 'IncludeController'
    InterleaveControl = 'InterleaveControl'
    RandomController = 'RandomController'
    RandomOrderController = 'RandomOrderController'
    RecordingController = 'RecordingController'
    RunTime = 'RunTime'
    ModuleController = 'ModuleController'
    SwitchController = 'SwitchController'