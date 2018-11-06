#
# Copyright (c) 2013-2018 Quarkslab.
# This file is part of IRMA project.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License in the top-level directory
# of this distribution and at:
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# No part of the project, including this file, may be copied,
# modified, propagated, or distributed except according to the
# terms contained in the LICENSE file.

import unittest
from copy import deepcopy
from irmacl_async.schemas import IrmaFileInfo, IrmaFileInfoSchema, \
    IrmaScan, IrmaScanSchema, \
    IrmaFileExt, IrmaFileExtSchema, \
    IrmaTag, IrmaTagSchema

file_infos_sample = {
    "mimetype": "EICAR virus test files",
    "sha1": "3395856ce81f2b7382dee72602f798b642f14140",
    "tags": [],
    "timestamp_first_scan": 1464531950.52,
    "timestamp_last_scan": 1488453424.26,
    "sha256":
    "275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f",
    "md5": "44d88612fea8a8f36de82e1278abb02f",
    "size": 68
}

probe_results_sample = {
    "antivirus": {
        "VirusBlokAda Console Scanner (Linux)": {
            "status": 1,
            "error": None,
            "results": "EICAR-Test-File",
            "version": "3.12.26.4",
            "duration": 3.04,
        }
    }
}

results_summary_sample = {
    "id": "d3347ebf-8589-488d-a867-3861237aef7d",
    "status": 1,
    "probes_finished": 1,
    "scan_id": "ae769a05-30a8-43f7-b97b-b97270916629",
    "parent_file_sha256": None,
    "name": "eicar.com",
    "scan_date": 1488453418,
    "probes_total": 1,
    "file_sha256":
        "275a021bbfb6489e54d471899f7db9d1663fc6'"
        "95ec2fe2a2c4538aabf651fd0f",
    "submitter": "cli",
}
results_sample = deepcopy(results_summary_sample)
results_sample['probe_results'] = probe_results_sample
results_sample['file_infos'] = file_infos_sample

scan_sample = {
    "status": 50,
    "probes_finished": 1,
    "force": True,
    "mimetype_filtering": True,
    "results": [results_summary_sample],
    "resubmit_files": True,
    "probes_total": 1,
    "date": 1488453418,
    "id": "ae769a05-30a8-43f7-b97b-b97270916629"
}

tag_sample = {
    "text": "malware",
    "id": 1
}


class IrmaMarshmallowTests(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_tag_serialization(self):
        tag = IrmaTag(**tag_sample)
        tag_dumps = IrmaTagSchema().dump(tag).data
        self.assertEqual(tag_dumps, tag_sample)

    def test_tag_deserialization(self):
        tag1 = IrmaTag(**tag_sample)
        tag_dumps = IrmaTagSchema().dump(tag1).data
        tag2 = IrmaTag(**tag_dumps)
        self.assertEqual(tag1.__dict__, tag2.__dict__)

    def test_file_infos_serialization(self):
        file_info = IrmaFileInfo(**file_infos_sample)
        file_info_dumps = IrmaFileInfoSchema().dump(file_info).data
        self.assertEqual(file_info_dumps, file_infos_sample)

    def test_file_infos_deserialization(self):
        file_info1 = IrmaFileInfo(**file_infos_sample)
        file_info_dumps = IrmaFileInfoSchema().dump(file_info1).data
        file_info2 = IrmaFileInfo(**file_info_dumps)
        self.assertEqual(file_info1.__dict__, file_info2.__dict__)

    def test_scan_serialization(self):
        scan = IrmaScan(**scan_sample)
        scan_dumps = IrmaScanSchema().dump(scan).data
        self.assertEqual(scan_dumps, scan_sample)

    def test_scan_deserialization(self):
        scan1 = IrmaScan(**scan_sample)
        scan_dumps = IrmaScanSchema().dump(scan1).data
        scan2 = IrmaScan(**scan_dumps)
        dict1 = deepcopy(scan1.__dict__)
        res1 = dict1.pop('results')
        dict2 = deepcopy(scan2.__dict__)
        res2 = dict2.pop('results')
        self.assertEqual(dict1, dict2)
        self.assertEqual(len(res1), len(res2))
        for r1, r2 in zip(res1, res2):
            self.assertEqual(r1, r2)

    def test_results_serialization(self):
        res = IrmaFileExt(**results_sample)
        res_dumps = IrmaFileExtSchema().dump(res).data
        print(results_sample)
        print(res_dumps)
        self.assertEqual(res_dumps, results_sample)

    def test_results_deserialization(self):
        res1 = IrmaFileExt(**results_sample)
        res_dumps = IrmaFileExtSchema().dump(res1).data
        res2 = IrmaFileExt(**res_dumps)
        dict1 = res1.__dict__.copy()
        dict1.pop("file_infos")
        dict1.pop("probe_results")
        probe_res1 = res1.probe_results
        file_infos1 = res1.file_infos
        dict2 = res2.__dict__.copy()
        probe_res2 = dict2.pop('probe_results')
        file_infos2 = dict2.pop('file_infos')
        self.assertEqual(dict1, dict2)
        self.assertEqual(file_infos1, file_infos2)
        self.assertEqual(len(probe_res1), len(probe_res2))
        self.assertEqual(probe_res1, probe_res2)
