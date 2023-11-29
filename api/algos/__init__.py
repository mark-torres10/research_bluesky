from . import attention, chronological, penalty

algos = {
    attention.uri: attention.handler,
    chronological.uri: chronological.handler,
    penalty.uri: penalty.handler,
}
