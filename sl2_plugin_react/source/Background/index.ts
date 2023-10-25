import 'emoji-log';
import {browser, Runtime} from 'webextension-polyfill-ts';
import {Instruction, MESSAGE_OPERATION} from '../interfaces/Instruction';
import {SEARCH_DISCIPLINES} from '../consts/search-schools-disciplines';
import {FilterListDto} from '../consts/filterlist-dto';
import {getAllFilters} from '../functions/api';
import {Filter} from '../models/filter';
import {loadFilterList} from '../functions/filters';
import {sortByPropertyName} from '../functions/utils';

let allFilterTags: Filter[];
let allFiltersDto: FilterListDto;
let selectedFilter: Filter;

const getCurrentTab = async () => {
  const allTabs = await browser.tabs.query({active: true, currentWindow: true});
  return allTabs[0];
};

async function readingFromClipboard(): Promise<string> {
  console.log('Hit');
  const text = await navigator.clipboard.readText();
  console.log('CLIPBOARD TEXT', text);
  return text;
}

const getUrl = (querySchool: string, discipline: string) => {
  return `https://www.google.com/search?q=${querySchool}+${discipline}+events`;
};

const setFilter = (filterId: string) => {
  const found = allFilterTags.find(
    (targetFilter) => targetFilter.entityId_Value === filterId
  );
  if (found) {
    selectedFilter = found;
  }
};

const searchTerm = (query) => {
  SEARCH_DISCIPLINES.forEach((discipline, index) => {
    // window.open(getUrl(query, discipline), '_blank');
    setTimeout(
      () => window.open(getUrl(query, discipline), '_blank'),
      1000 * index + 1
    );
  });
};

const backgroundReducer = async (message, sender): Promise<any | undefined> => {
  let response = '';
  console.log('Background Receive:', {message, sender});
  let tab;
  switch ((message as Instruction).operation) {
    case MESSAGE_OPERATION.GET_CURRENT_TAB_ID:
      tab = await getCurrentTab();
      return tab.id;
    case MESSAGE_OPERATION.GET_CURRENT_TAB_URL:
      tab = await getCurrentTab();
      return tab?.url;
    case MESSAGE_OPERATION.SELECT_A_FILTER:
      setFilter((message as Instruction).payload);
      return;
    case MESSAGE_OPERATION.GET_SELECTED_FILTER:
      return selectedFilter;
    case MESSAGE_OPERATION.GET_ALL_FILTERS_DTO:
      return allFiltersDto;
    case MESSAGE_OPERATION.GET_ALL_FILTERS:
      return allFilterTags;
    case MESSAGE_OPERATION.TEST:
      test(message, sender);
      return;
    case MESSAGE_OPERATION.READ_FROM_CLIPBOARD:
      console.log('Hit');
      response = await navigator.clipboard.readText();
      console.log('CLIPBOARD TEXT', response);
      return response;
    case MESSAGE_OPERATION.SEARCH:
      searchTerm(message.payload);
      break;
  }

  // console.log("Background prvodeds current tab id", tabId)
};

browser.commands.onCommand.addListener(function (command) {
  console.log(command);
});

browser.runtime.onInstalled.addListener((): void => {
  console.emoji('🦄', 'extension installed');
});

browser.runtime.onMessage.addListener(backgroundReducer);

const test = async (message: Instruction, sender: Runtime.MessageSender) => {
  console.log('Testing haha', message, sender);
  // const result = await browser.cookies.getAll;
  // console.log(result)
  // const newLead = Object.assign(new Lead(), {
  //   url: 'new test',
  // });
  // const result = await postLead(newLead);
  // console.log('Background posted', result);
};

// load all filters tags
async function init(): Promise<void> {
  const result = await getAllFilters();
  if (result) {
    allFiltersDto = {...result};
    allFiltersDto.organizations = sortByPropertyName(
      allFiltersDto.organizations,
      {sortProperty: 'name', sortOrder: 'asc'}
    );
    allFilterTags = loadFilterList(allFiltersDto);
    console.log(allFilterTags);

    // sort alfilters dto's organization list
  } else {
    console.error('Unable to get all filters');
  }

}



init();
