version=0.0

script_dir=$(dirname "$0")
img_name=srb-translit:${version}

# build image
docker build -t ${img_name} ${script_dir}

# check image size
docker images | grep ${img_name}

echo "To run image:"
echo "    docker run -it -v ${script_dir}/..:/test_root srb-translit:${version}"

