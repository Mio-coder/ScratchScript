from lang_function import get_raw_fn, get_spec


def get_motion():
    motion_spec = get_spec("MotionBlocks")
    functions = dict()
    functions["turnleft"] = get_raw_fn(motion_spec["motion_turnleft"])
    functions["goto"] = get_raw_fn(motion_spec["motion_goto"])
    functions["goto_menu"] = get_raw_fn(motion_spec["motion_goto_menu"])
    functions["glidesecstoxy"] = get_raw_fn(motion_spec["motion_glidesecstoxy"])
    functions["pointindirection"] = get_raw_fn(motion_spec["motion_pointindirection"])
    functions["pointtowards"] = get_raw_fn(motion_spec["motion_pointtowards"])
    functions["pointtowards_menu"] = get_raw_fn(motion_spec["motion_pointtowards_menu"])
    functions["changexby"] = get_raw_fn(motion_spec["motion_changexby"])
    functions["setx"] = get_raw_fn(motion_spec["motion_setx"])
    functions["changeyby"] = get_raw_fn(motion_spec["motion_changeyby"])
    functions["sety"] = get_raw_fn(motion_spec["motion_sety"])
    functions["ifonedgebounce"] = get_raw_fn(motion_spec["motion_ifonedgebounce"])
    functions["setrotationstyle"] = get_raw_fn(motion_spec["motion_setrotationstyle"])
    functions["xposition"] = get_raw_fn(motion_spec["motion_xposition"])
    functions["yposition"] = get_raw_fn(motion_spec["motion_yposition"])
    functions["direction"] = get_raw_fn(motion_spec["motion_direction"])
    functions["gotoxy"] = get_raw_fn(motion_spec["motion_gotoxy"])
    functions["glideto"] = get_raw_fn(motion_spec["motion_glideto"])
    functions["glideto_menu"] = get_raw_fn(motion_spec["motion_glideto_menu"])
    return {"motion": functions}
