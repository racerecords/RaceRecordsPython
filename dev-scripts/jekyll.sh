#! /bin/bash
cd ..
export JEKYLL_VERSION=3.8
options='--name jekyll --rm -p 4000:4000'
case $1 in
	build)
		cmd='jekyll build'
	;;
	bash)
		cmd='/bin/bash'
	;;
	background)
		cmd='jekyll server 0.0.0.0'
		options="$options -d"
	;;
	*)
		cmd='jekyll server 0.0.0.0'
	;;
esac
docker run $options -v jekyll-gems:/usr/local/bundle  --volume="$PWD/jekyll:/srv/jekyll" -it jekyll/jekyll:$JEKYLL_VERSION $cmd
