// import http from 'k6/http';
// import { sleep } from 'k6';
//
// export default function () {
//   http.get('http://localhost:8000/webinars/month_uncached/');
//   sleep(1);
// }

import http from 'k6/http';
import { sleep } from 'k6';
export let options = {
  vus: 500,
  duration: '10s',
};
export default function () {
  http.get('http://localhost:8000/webinars/month_uncached/');
  sleep(1);
}