cd streamlit
streamlit run main.py --server.sslCertFile=rsc/host.cert --server.sslKeyFile=rsc/host.key
cd frontend
npm run dev