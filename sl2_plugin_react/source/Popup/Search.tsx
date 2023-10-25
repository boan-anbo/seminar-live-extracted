import * as React from 'react';
import {useEffect, useState} from 'react';
import {isLoggedIn} from '../functions/auth';
import {searchBrowserEngine} from '../functions/search';
import {Organization} from '../models/organization';
import {
  getAllFilterDtoFromBackground,
  getSelectedFilterFromBackground,
  setSelectedFilterToBackground,
} from '../functions/filters';
import {getTabUrl} from '../functions/tabs';
import {SEARCH_DISCIPLINES} from '../consts/search-schools-disciplines';
import {sortByPropertyName} from '../functions/utils';

const Search: React.FC = () => {
  const [allOrganizations, setAllOrganizations] = useState<Organization[]>([]);

  const [selectedOrgName, setSelectedOrgName] = useState<string>('');

  const [selectedOrgId, setSelectedOrgId] = useState<string>('');

  const handleSearchChange = (event) => {
    setSelectedOrgName(event.target.value);
  };

  const searchTerm = (additionalQuery?: string) => {
    searchBrowserEngine(`${selectedOrgName} ${ additionalQuery ? additionalQuery : ''}`);
  };

  const handleSearchSchoolOnGoogle = async () => {
    await searchTerm();
  };

  const handleSearchOnEventbriteOrganization = async () => {
    await searchTerm('eventbrite organizer');
  };

  const setSelectedFilterFromLocalToBackground = async (filterId: string) => {
    await setSelectedFilterToBackground(filterId);
  };

  const setSchoolName = (schoolName: string) => {
    setSelectedOrgName(schoolName);
  };

  const loadAllFiltersFromBackground = async () => {
    const filtersDto = await getAllFilterDtoFromBackground();
    console.log('Popup Received Filters Dto', filtersDto);

    setAllOrganizations(filtersDto.organizations);
    console.log(filtersDto);
  };

  const loadSelectedFilter = async () => {
    const selectedFilter = await getSelectedFilterFromBackground();
    if (selectedFilter) {
      const {name, id} = selectedFilter.entity as Organization;
      setSelectedOrgId(id);
      setSchoolName(name);
    }
  };

  useEffect(() => {
    loadAllFiltersFromBackground();

    loadSelectedFilter();
  }, []);

  const setLocalSelectedOrganization = (event) => {
    const targetOrganization: Organization | undefined = allOrganizations.find(
      (targetOrg) => targetOrg.id === event.target.value
    );
    if (targetOrganization) {
      setSchoolName(targetOrganization.name);
      setSelectedOrgId(targetOrganization.id);
      setSelectedFilterFromLocalToBackground(targetOrganization.id);
    }
  };

  return (
    <div>
      {
        <div>
          <div>
            <label>
              Pick a school
              <select
                name="schools"
                value={selectedOrgId}
                onChange={setLocalSelectedOrganization}
              >
                {allOrganizations.map((organization, index) => {
                  return (
                    <option key={organization.id} value={organization?.id}>
                      {organization?.name}
                    </option>
                  );
                })}
              </select>
            </label>
          </div>

          <label>
            Search School:
            <input
              type="text"
              value={selectedOrgName}
              onChange={handleSearchChange}
            />
          </label>
          <div />
          <div>
            <button onClick={handleSearchSchoolOnGoogle}>
              Search School On Google
            </button>
          </div>

          <div>
            <button onClick={handleSearchOnEventbriteOrganization}>
              Search Eventbrite Org on Google{' '}
            </button>
          </div>

          <ol>
            {SEARCH_DISCIPLINES.map((discipline, index) => {
              return <dt>{discipline}</dt>;
            })}
          </ol>
        </div>
      }
    </div>
  );
};

export default Search;
