export const fetchAccountInfo = async () => {
    try {
      const response = await fetch('http://localhost:5000/account/info', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,  // Sử dụng backticks cho template literal
        },
      });
  
      if (response.ok) {
        const accountInfo = await response.json();
        localStorage.setItem('account_id', accountInfo.account_id);
        localStorage.setItem('balance', accountInfo.balance);
        return accountInfo;
      } else {
        console.error('Failed to fetch account info');
        return null;
      }
    } catch (error) {
      console.error('Error fetching account info:', error);
      return null;
    }
  };
  