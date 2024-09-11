import axios from "axios";

const BITCOIN_ADDRESS = "your_bitcoin_address_here";
const API_URL = `https://blockchain.info/rawaddr/${BITCOIN_ADDRESS}`;

const getAddressInfo = async () => {
  try {
    const response = await axios.get(API_URL);
    return response.data;
  } catch (error) {
    console.error(`Error fetching data: ${error}`);
    return null;
  }
};

const monitorAddress = async () => {
  let previousTxCount: number | null = null;

  while (true) {
    const data = await getAddressInfo();
    if (data) {
      const txCount = data.txs.length;
      if (previousTxCount === null) {
        previousTxCount = txCount;
      } else if (txCount > previousTxCount) {
        console.log(`New transaction detected! Total transactions: ${txCount}`);
        previousTxCount = txCount;
      } else {
        console.log(`No new transactions. Total transactions: ${txCount}`);
      }
    }

    await new Promise((resolve) => setTimeout(resolve, 60000)); // Check every 60 seconds
  }
};

monitorAddress();
