mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"your-email@domain.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml

echo "\
[theme]\n\
primaryColor = \"#c57316\"\n\
backgroundColor = \"#00172B\"\n\
secondaryBackgroundColor = \"#0083B8\"\n\
textColor = \"#FFF\"\n\
font = \"sans serif\"\n\
" > ~/.streamlit/config.toml