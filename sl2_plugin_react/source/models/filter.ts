import {Person} from './person';
import {Tag} from './tag';
import {Organization} from './organization';
import {Host} from './host';

export enum FILTER_TYPE {
  organizer = 'organizers',
  tag = 'tags',
  speaker = 'talks__speakers__person',
  hasRecordingOrTranscript = 'hasRecordingOrTranscript',
  organization = 'hosts__organizations',
  host = 'hosts',
  mainFilterType = 'main_filter_type',
  mainFilterSlugName = 'main_filter_slugname'

}






export class Filter {
  filterType: FILTER_TYPE;
  entity?: FilterEntityType;
  // ID: example: Tag id, person id. Value example: True for 'hasRecordingOrTranscript'
  entityId_Value: string;
  entitySlugName: string;


  constructor(filterType: FILTER_TYPE, slugName?: string, idOrValue?: string, entity?: FilterEntityType) {
    try {
      this.filterType = filterType;

      if (slugName) {
        this.entitySlugName = slugName;
      }

      if (entity) {
        this.entity = entity;
        if (!this.entitySlugName && entity.slugName) {
          this.entitySlugName = entity.slugName
        }
      }

      if (idOrValue) {
        this.entityId_Value = idOrValue;
      }


    } catch (e) {
      throw new Error('cannot construct filter out of the given entity');
    }
  }
}


export type FilterEntityType = Tag | Person | Host | Organization;
