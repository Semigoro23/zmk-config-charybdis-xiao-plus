zephyr_library()
zephyr_library_sources_ifdef(CONFIG_Y13_XIAO_LOW_CHARGE src/charge.c)
