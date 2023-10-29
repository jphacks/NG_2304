import axios from 'lib/axios';
import { useEffect } from 'react';
import getLayout from '@/components/layouts/main';
import { useRouter } from 'next/router';

const Callback = () => {
  const router = useRouter();
  const { query } = router;
  useEffect(() => {
    if (router.isReady) {
      const { seal } = query;
      axios
        .post('/api/token', {
          seal,
        })
        .finally(() => {
          router.replace('/');
        });
    }
  }, [router, query]);
};

Callback.getLayout = getLayout;

export default Callback;
