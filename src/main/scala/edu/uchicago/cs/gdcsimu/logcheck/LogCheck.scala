package edu.uchicago.cs.gdcsimu.logcheck

import scala.io.Source
import scala.collection.mutable.ArrayBuffer

object LogCheck extends App {
  var datas = new ArrayBuffer[Array[Int]]();
  Source.fromFile("src/main/resource/MISO_oneday_trace.csv").getLines().foreach { line =>
    {
      var content = line.split(",")
      datas += content(1).toCharArray().map(_ match { case '0' => 0 case _ => 1 })
    }
  }

  // Look for single max
  datas.zipWithIndex.foreach(t => {
    System.out.println("%d:%d".format(t._2, t._1.sum))
  })

  var max2 = (0, 0);
  var maxsum = 0;
  var lstpnter: Array[Int] = null;
  // Look for 2 combine max
  for (i <- 0 until 6) {
    for (j <- i until 6) {
      var lst = datas(i).zip(datas(j)).map(a => (a._1 + a._2) match { case 0 => 0 case _ => 1 })
      var sum = lst.sum
      if (maxsum < sum) {
        maxsum = sum
        max2 = (i, j)
        lstpnter = lst;
      }
    }
  }

  System.out.println("%d,%d:%d".format(max2._1, max2._2, maxsum))
  System.out.println(lstpnter.mkString(","))

  System.out.println(datas(max2._1).sliding(6, 6).map { _.sum match { case x if x <= 3 => 0 case _ => 1 } }.mkString(""))
  System.out.println(datas(max2._2).sliding(6, 6).map { _.sum match { case x if x <= 3 => 0 case _ => 1 } }.mkString(""))
  System.out.println(lstpnter.sliding(6, 6).map { _.sum match { case x if x <= 3 => 0 case _ => 1 } }.mkString(""))

  var max3 = (0, 0, 0);
  maxsum = 0;
  // Look for 2 combine max
  for (i <- 0 until 6) {
    for (j <- i until 6) {
      for (k <- j until 6) {
        var lst = datas(i).zip(datas(j)).zip(datas(k))
          .map(a => ((a._1._1 + a._1._2 + a._2 match { case 0 => 0 case _ => 1 })))
        var sum = lst.sum
        if (maxsum < sum) {
          maxsum = sum
          max3 = (i, j, k)
          lstpnter = lst
        }
      }
    }
  }

  System.out.println("%d,%d,%d:%d".format(max3._1, max3._2, max3._3, maxsum))
  System.out.println(lstpnter.mkString(","))
  System.out.println(lstpnter.sliding(6, 6).map { _.sum match { case x if x <= 3 => 0 case _ => 1 } }.mkString(","))

}