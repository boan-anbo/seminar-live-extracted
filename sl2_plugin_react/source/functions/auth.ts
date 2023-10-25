import {getKey} from './cookie';

export const isLoggedIn = (): boolean => {
  return getKey()?.length > 0;
};

