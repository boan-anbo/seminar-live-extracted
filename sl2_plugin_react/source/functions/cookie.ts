import Cookies from 'js-cookie';

const keyName = 'sl2_key';

export const saveKey = (key: string) => {
  Cookies.set(keyName, key, {expires: 7});
};

export const getKey = () => {
  return Cookies.get(keyName);
};

export const clearKey = () => {
  Cookies.remove(keyName);
};
