# coding=utf8

import json
from pprint import pprint
from collections import OrderedDict
import os

herb_features = ["ปวดศรีษะ", "หวัดคัดจมูก", "ไข้", "ไอ", "ร้อนใน", "กระหายน้ำ", "ปวดหู", "ยาระบาย", "บำรุงน้ำดี", "คัน", "โรคผิวหนัง", "ฆ่าเชื้อ", "ฟกซ้ำ", "บวมอักเสบ", "อาการป็นลม", "บำรุงหัวใจ", "โรคสันนิบาต", "อาหารวิงเวียนศรีษะ", "ขับลม", "ขับเสมหะ", "น้ำหอมติดเสื้อ", "ลดน้ำตาลในเส้นเลือด", "ผมหงอก", "ไข้ทับระดู", "พิษเมา", "ปวดท้อง", "อีสุกอีใส", "มาลาเรีย", "ขับพิษ", "ชะลอวัย", "บำรุงกำลัง", "ลดความอ้วน", "ลดไขมันในเส้นเลือด", "ป้องกันมะเร็ง", "ลดความดัน", "บำรุงตับ", "บำรุงไต", "อัมพฤกษ์", "ชักเกร็ง", "บำรุงผิว", "เวียนศรีษะ", "โรคเบาหวาน", "ปวดตามกล้ามเนื้อ", "เหงือกอักเสบ", "บำรุงสายตา", "ไซนัสอักเสบ", "ลดการนอนกรน", "โรคหอบหืด", "ปวดมดลูก", "ตับอักเสบ", "ท้องเสีย", "ท้องผูก", "โรคกระเพาะ", "ลำไส้อักเสบ", "ปัสสาวะขัด", "มดลูกโต", "ต่อมลูกหมากโต", "ตกขาว", "โรคเกาต์", "พิษแมลงสัตว์กัดต่อย", "ท้องอืด", "ท้องเฟ้อ", "กรดในกระเพาะอาหาร", "มดลูกอักเสบ", "ปวดเมื่อย", "นอนหลับสบาย", "กระตุ้นความต้องการทางเพศ", "กระตุ้นผลิตอสุจิ", "เพิ่มฮอร์โมนเพศ", "ผิวพรรณเปล่งปลั่ง", "กระชับช่องคลอด", "โรคพาร์กินสัน", "หนองใน", "คอพอก", "กระตุ้นระบบประสาท", "ตามัว", "กลากเกลื้อน", "ผื่นคัน", "ลดการบวมของแผล", "ผมร่วง", "พิษฝีภายใน", "พิษในกระดูก", "น้ำเหลืองเสีย", "เหงือกและฟัน", "โลหิตเป็นพิษ", "เจริญอาหาร", "คลื่นไส้อาเจียน", "ขับเลือด", "ขับรก", "ปวดประจำเดือน", "งูกัด", "สะอึก", "ดีซ่าน", "ริดสีดวงทวาร", "ตาเหลือง", "ขับพยาธิ", "ฝีแผลพุพอง", "โรคปอด", "เพิ่มภูมิต้านทาน", "ภูมิแพ้", "เบาหวาน", "น้ำตาในเลือด", "นอนกรน", "ฝีภายใน", "เอ็นพิการ", "รากผม", "ผมเงางาม", "สมานแผล", "ลดกรดในกระเพาะอาหาร", "โรคทางเดินปัสสาวะ", "ขับปัสสาวะ", "เพิ่มน้ำนม", "สานตะกร้า", "เสื่อ", "เชือก", "กระดาษ", "กำจัดคราบน้ำมัน", "บำบัดน้ำเสีย", "เลือดลมไหลเวียนดี", "ยาฟอกเลือด", "ธาตุพิการ", "ขับน้ำลาย", "ปากเปื่อย", "ปากเป็นแผล", "ปากซีด", "ฆ่าพยาธิ", "ฆ่าเชื้อโรคภายใน", "ท่อน้ำดีอักเสบ", "ขับน้ำดี", "ตัวเหลือง", "ตาเหลือง", "ช้ำใน", "ถ่ายพิษไข้", "คออักเสบ", "เจ็บคอ", "ปวดท้องน้อย", "ชะลอการเกิดริ้วรอย", "สร้างภูมิต้านทาน", "โรคมะเร็ง", "ลดคอเลสเตอรอล", "กำจัดสารพิษ", "โรคความดันโลหิตสูง", "ขับน้ำนม", "บำรุงสมอง", "โรครูมาตอยด์", "แพ้", "ป้องกันการแข็งตัวของหลอดเลือด", "แผลที่ปาก", "บำรุงปอด", "จุคเสียด", "แน่นท้อง", "ลำไส้ใหญ่บวม", "นิ่วในถุงน้ำดี", "ทำความสะอาดลำไส้", "ตับอ่อนอักเสบ", "ตกเลือด", "ผิวหนังพุพอง", "สิวผด", "สิวอุดตัน", "สิวเสี้ยน", "แผลในกระเพาะอาหาร", "กระเพาะลำไส้อักเสบ", "ระดูขาว", "ขับน้ำคาวปลา", "ปวดตามข้อ", "ฝี", "แผลสด", "แผลถลอก", "แผลไฟไหม้", "น้ำร้อนลวก", "ดับพิษร้อน", "ปวดแสบปวดร้อน", "รอยแผลเป็น", "ตาปลา", "ฮ่องกงฟุต", "ผิวหนังแห้ง", "ฝ้า", "สะเก็ดเงิน", "ลดแบคทีเรียในลำไส้", "ช่วยย่อยอาหาร", "ผิวแห้ง", "ผิวชุ่มชื้น", "ลดริ้วร้อย", "ลดรอยดำ", "ผมดก", "ลบท้องลาย", "เส้นเลือดดำขอด", "ยาอายุวัฒนะ", "สดชื่น", "ฟื้นฟูเซลล์", "ปรับสมดุลร่างกาย", "เผาผลาญไขมัน", "โรคหัวใจ", "อ่อนล้า", "อ่อนเพลีย", "เนื้องอก", "เชื้อมาลาเรีย", "ปากคอแห้ง", "งูสวัด", "โรคเริม", "ส้นเท้าแตก"]

herb_json_array = None

with open(os.path.join('data', 'herb_data.json'), encoding="utf-8") as f:
    herb_json_array = json.load(f)

# herb_data[0]['label'] = "ทดสอบ"
pprint(herb_json_array[0])

for herb_object in herb_json_array:
    feature_list = []
    for benefit in herb_object['benefitList']:
        for feature in herb_features:
            if feature in benefit:
                feature_list.append(feature)
        # print(benefit)
    for property in herb_object['propertyList']:
        for feature in herb_features:
            if feature in property:
                feature_list.append(feature)
        # print(property)
    unique_feature_list = list(OrderedDict.fromkeys(feature_list))
    herb_object['featureList'] = unique_feature_list

with open(os.path.join('data', 'herb_data_labeled.json'), 'w', encoding="utf-8") as outfile:
    json.dump(herb_json_array, outfile, ensure_ascii=False)

# pprint(data)
