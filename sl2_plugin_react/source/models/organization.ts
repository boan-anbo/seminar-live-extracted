import {FilterAbstractEntity} from "./abstract-filter";

export class Organization implements FilterAbstractEntity {
  id: string;
  slugName: string;
  timezone: string;
  color: string;
  name: string;
  nameCn: string;
  nameShortCn: string;
  nameShort: string;

}
