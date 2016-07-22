#!/usr/bin/python
# -*- coding: utf-8 -*-

from blog import blog
if __name__ == "__main__":
	
	blog.run(debug = True, host='0.0.0.0', port=9000)
