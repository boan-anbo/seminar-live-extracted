import {Instruction, MESSAGE_OPERATION} from '../interfaces/Instruction';
import {instruct} from './message';
import {FilterListDto} from '../consts/filterlist-dto';
import {Filter, FILTER_TYPE} from '../models/filter';

export const getAllFiltersFromBackground = async (): Promise<Filter[]> => {
  return instruct({
    operation: MESSAGE_OPERATION.GET_ALL_FILTERS,
  } as Instruction);
};

export const getAllFilterDtoFromBackground = async (): Promise<FilterListDto> => {
  return instruct({
    operation: MESSAGE_OPERATION.GET_ALL_FILTERS_DTO,
  } as Instruction);
};

export const getSelectedFilterFromBackground = async (): Promise<Filter> => {
  return instruct({
    operation: MESSAGE_OPERATION.GET_SELECTED_FILTER,
  } as Instruction) as Promise<Filter>;
}

export const setSelectedFilterToBackground = async (filterId: string) => {
  return instruct({
    payload: filterId,
    operation: MESSAGE_OPERATION.SELECT_A_FILTER,
  } as Instruction);
}





export function loadFilterList(filterListDto: FilterListDto): Filter [] {
  const allFilters: Filter[] = [];
  filterListDto.hosts.forEach(host => {
    const newFilter = new Filter(FILTER_TYPE.host, undefined, host.id, host);
    allFilters.push(newFilter);
  });
  filterListDto.organizations.forEach(organization => {
    const newFilter = new Filter(FILTER_TYPE.organization, undefined, organization.id, organization);
    allFilters.push(newFilter);
  });
  filterListDto.tags.forEach(tag => {
    const newFilter = new Filter(FILTER_TYPE.tag, undefined, tag.id, tag);
    allFilters.push(newFilter);
  });


  return allFilters;
}

