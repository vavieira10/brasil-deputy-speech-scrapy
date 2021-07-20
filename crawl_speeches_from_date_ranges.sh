for ((i=$1;i<=$2;i++)); do
    make crawl-site-speeches year=$i 
done