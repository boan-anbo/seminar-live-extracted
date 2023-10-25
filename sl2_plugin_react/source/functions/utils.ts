import sorta from 'array-sort';




export type SortOrder = 'asc' | 'desc';

export interface SortInstruction {
  sortOrder: SortOrder;
  sortProperty: string;
}



export const titleCase = (s) =>
  s.replace (/^[-_]*(.)/, (_, c) => c.toUpperCase())       // Initial char (after -/_)
    .replace (/[-_]+(.)/g, (_, c) => ' ' + c.toUpperCase()) // First char after each -/_


/**
 *
 * @param collection
 * @param sortInstruction: sortOrder: 'asc' or 'desc'. sortProperty.
 * @return sorted collection
 */
export function sortByPropertyName<T>(collection: T[], sortInstruction: SortInstruction): T[] {
  switch (sortInstruction?.sortOrder) {
    case 'asc':
      return sorta(collection, sortInstruction.sortProperty);
    case 'desc':
      console.log('revesed');
      return sorta(collection, sortInstruction.sortProperty).reverse();
  }

}
