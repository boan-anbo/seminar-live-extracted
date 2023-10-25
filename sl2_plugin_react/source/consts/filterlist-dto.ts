import {Tag} from '../models/tag';
import {Organization} from '../models/organization';
import {Host} from '../models/host';

export interface FilterListDto {
  hosts: Host[];
  organizations: Organization[];
  tags: Tag[];
}
