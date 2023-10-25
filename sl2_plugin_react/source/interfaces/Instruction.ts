export enum MESSAGE_OPERATION {
    'GET_CURRENT_TAB_ID',
    'GET_CURRENT_TAB_URL',
    'TEST',
    GET_DOM_HTML,
    GET_TABID_FROM_CONTENT,
    SEARCH,
    'GET_ALL_FILTERS',
    GET_ALL_FILTERS_DTO,
    SELECT_A_FILTER,
    GET_SELECTED_FILTER,
    READ_FROM_CLIPBOARD,
}


export class Instruction {
    operation?: MESSAGE_OPERATION
    payload?: any
}

