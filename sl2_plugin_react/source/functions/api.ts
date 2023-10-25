import axios from 'axios';
import {Lead} from '../interfaces/lead';
import {clearKey, getKey, saveKey} from './cookie';
import {isLoggedIn} from './auth';
import {FilterListDto} from '../consts/filterlist-dto';
import {Source} from '../models/source';

export const BASE_URL = 'https://www.seminar-live.org/api/';
// export const BASE_URL = 'http://localhost:8000/';
export const APIS = {
  postLead: `${BASE_URL}leads/`,
  login: `${BASE_URL}auth/login/`,
  logout: `${BASE_URL}auth/logout/`,
  allFilters: `${BASE_URL}webinars/get_all_filters/`,
  postSource: `${BASE_URL}sources/`,
};

export const postSource = async (source: Source): Promise<any> => {
  // axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
  // axios.defaults.xsrfCookieName = "csrftoken";

  axios.defaults.withCredentials = true;

  // const formLead = new FormData();
  // // formLead.append('file', lead.file ?? '');
  // formLead.append('text', lead.text ?? '');
  // formLead.append('url', lead.url ?? '');
  // formLead.append('html', lead.html ?? '');
  // if (lead.hostOrganizations && lead.hostOrganizations?.length > 0) {
  //  formLead.append('hostOrganizations', lead.hostOrganizations)
  // }

  const result = await axios.post(APIS.postSource, source, {
    xsrfCookieName: 'csrftoken',
    xsrfHeaderName: 'X-CSRFToken',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Token ${getKey()}`,
    },
  });

  console.log('Post Result', result);
  return result;
};

export const postLead = async (lead: Lead): Promise<any> => {
  // axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
  // axios.defaults.xsrfCookieName = "csrftoken";

  axios.defaults.withCredentials = true;

  const formLead = new FormData();
  // formLead.append('file', lead.file ?? '');
  formLead.append('text', lead.text ?? '');
  formLead.append('url', lead.url ?? '');
  formLead.append('html', lead.html ?? '');
  // if (lead.hostOrganizations && lead.hostOrganizations?.length > 0) {
  //  formLead.append('hostOrganizations', lead.hostOrganizations)
  // }

  const result = await axios.post(APIS.postLead, lead, {
    xsrfCookieName: 'csrftoken',
    xsrfHeaderName: 'X-CSRFToken',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Token ${getKey()}`,
    },
  });

  console.log('Post Result', result);
  return result;
};

export const login = async (payload: {password: string; email: string}) => {
  console.log('sending');

  try {
    axios.defaults.withCredentials = true;
    axios.defaults.xsrfCookieName = 'csrftoken';
    axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN';
    const {data} = await axios.post(APIS.login, payload, {
      headers: {
        'Content-Type': 'application/json',
      },
    });
    console.log(data);
    const {key} = data;
    saveKey(key);
    console.log('saved Key', getKey());
  } catch (e) {
    console.log({e});
  }
};

export const logout = async () => {
  try {
    if (!isLoggedIn()) {
      return;
    }
    const result = await axios.post(
      APIS.logout,
      {},
      {
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Token ${getKey()}`,
        },
      }
    );
    if (result?.status === 200) {
      clearKey();
    }
  } catch (e) {
    console.log({e});
    clearKey();
  }
};

export const getAllFilters = async () => {
  try {
    const {data} = await axios.get<FilterListDto>(APIS.allFilters);

    return data;
  } catch (e) {
    console.warn('Unable to fetch filters', {e});
    return null;
  }
};
