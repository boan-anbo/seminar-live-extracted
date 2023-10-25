import {Organization} from './organization';
import {FilterAbstractEntity} from "./abstract-filter";

export class Host implements FilterAbstractEntity {
  id: string;
  name: string;
  nameCn: string;
  nameShortCn: string;
  color: string;
  nameShort: string;
  slugName: string;
  organizations: Organization [];
  timezone: string;
}
