import {FilterAbstractEntity} from "./abstract-filter";

export class Tag implements FilterAbstractEntity {
  id: string;
  tagName = '';
  tagNameCn = '';
  slugName = '';
  tagType: TagType =  'DISCIPLINE';
}

export type TagType = 'DISCIPLINE' | 'TOPIC' | 'LANGUAGE' | 'AREA';
