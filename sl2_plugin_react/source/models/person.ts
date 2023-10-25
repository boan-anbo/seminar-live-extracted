import {FilterAbstractEntity} from "./abstract-filter";

export class Person implements  FilterAbstractEntity {
  id: string;
  lastName: string;
  firstName: string;
  slugName: string;
  organizerWebinars: string[];
}
