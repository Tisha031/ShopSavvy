-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 20, 2025 at 09:39 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `trumart_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `add_to_bag`
--

CREATE TABLE `add_to_bag` (
  `bag_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `cust_id` int(11) NOT NULL,
  `qty` int(11) NOT NULL,
  `custom_image` varchar(500) NOT NULL,
  `date` date NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `add_to_cart`
--

CREATE TABLE `add_to_cart` (
  `cart_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `prdct_id` int(11) NOT NULL,
  `qty` int(11) NOT NULL DEFAULT 1,
  `date` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `admin_login`
--

CREATE TABLE `admin_login` (
  `Admin_id` int(11) NOT NULL,
  `Email` varchar(15) NOT NULL,
  `Password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin_login`
--

INSERT INTO `admin_login` (`Admin_id`, `Email`, `Password`) VALUES
(1, 'admin@gmail.com', 'admin1');

-- --------------------------------------------------------

--
-- Table structure for table `customization`
--

CREATE TABLE `customization` (
  `cust_id` int(11) NOT NULL,
  `prdct_name` varchar(50) NOT NULL,
  `price` int(11) NOT NULL,
  `img` varchar(500) NOT NULL,
  `description` varchar(500) NOT NULL,
  `qty` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `customization`
--

INSERT INTO `customization` (`cust_id`, `prdct_name`, `price`, `img`, `description`, `qty`) VALUES
(2, 'T-shirt', 759, 'static/upload/Fit-Polo-T-shirt.png', 'white polo T-shirt', 2);

-- --------------------------------------------------------

--
-- Table structure for table `feedback`
--

CREATE TABLE `feedback` (
  `user_id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `feed_cat` varchar(50) NOT NULL,
  `feed_des` varchar(500) NOT NULL,
  `img` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `feedback`
--

INSERT INTO `feedback` (`user_id`, `name`, `email`, `feed_cat`, `feed_des`, `img`) VALUES
(2, 'tisha jinger', 'tishajinger0310@gmail.com', 'Website Exp', 'better UI', '');

-- --------------------------------------------------------

--
-- Table structure for table `manage_cat`
--

CREATE TABLE `manage_cat` (
  `cat_id` int(11) NOT NULL,
  `cat_name` varchar(50) NOT NULL,
  `description` varchar(200) NOT NULL,
  `supp_id` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `manage_cat`
--

INSERT INTO `manage_cat` (`cat_id`, `cat_name`, `description`, `supp_id`) VALUES
(12, 'Men', 'Men\'s wear', 0),
(13, 'Woman', 'Women\'s wear', 0),
(14, 'Kids', 'kid\'s wear', 0);

-- --------------------------------------------------------

--
-- Table structure for table `manage_disp`
--

CREATE TABLE `manage_disp` (
  `disp_id` int(11) NOT NULL,
  `name` varchar(15) NOT NULL,
  `mobile` varchar(15) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(20) NOT NULL,
  `status` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `manage_disp`
--

INSERT INTO `manage_disp` (`disp_id`, `name`, `mobile`, `email`, `password`, `status`) VALUES
(12, 'mansi', '8200517195', 'mansi2@gmail.com', 'mansi122', 1),
(15, 'Jenish Patel', '9984349870', 'PJenish04@gmail.com', 'JenishP@te!991', 0);

-- --------------------------------------------------------

--
-- Table structure for table `manage_prdct`
--

CREATE TABLE `manage_prdct` (
  `prdct_id` int(11) NOT NULL,
  `cat_id` int(50) NOT NULL,
  `prdct_name` varchar(25) NOT NULL,
  `price` decimal(10,0) NOT NULL,
  `p_image` varchar(500) DEFAULT NULL,
  `description` varchar(200) NOT NULL,
  `qty` bigint(11) NOT NULL DEFAULT 0,
  `supp_id` int(11) NOT NULL,
  `subcat_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `manage_prdct`
--

INSERT INTO `manage_prdct` (`prdct_id`, `cat_id`, `prdct_name`, `price`, `p_image`, `description`, `qty`, `supp_id`, `subcat_id`) VALUES
(29, 13, 'ShopSavvy X Grow With The', 799, 'static/upload/over_puff_print.png', 'Shop for Grow With The Flow Women Oversized T-Shirts at The ShopSavvy Store.', 5, 0, 25),
(30, 14, 'Denim dungarees', 1499, 'static/upload/denim_blue.png', 'Dungarees in washed denim featuring straps with adjustable press-studs, press-studs at the sides and a fake fly', 4, 0, 27),
(31, 12, 'ShopSavvy X NXT GEN', 699, 'static/upload/green_nxt_gen_short.png', 'Men\'s Green Typography Side Vent Oversized Shorts', 0, 0, 10),
(32, 12, 'ShopSavvy X Charcoal Grey', 999, 'static/upload/men-s-charcoal-grey_jooggers.png', 'Baggy and cool, these joggers make styling super easy', 0, 0, 7),
(33, 13, 'ShoopSaavy X Purple Super', 899, 'static/upload/womens_purple-fit-cargo.png', 'Super Loose fit - Super Loose On Body Thoda Hawa Aane De Terry - Soft & Durable', 0, 0, 26),
(34, 13, 'ShopSavvy X DISNEY', 699, 'static/upload/disney.png', 'Black Mickey Graphic Printed Oversized T-shirt', 0, 0, 25),
(35, 12, 'Grey Oversized Pyjamas', 699, 'static/upload/grey-pyjamas.png', 'Because who needs fitted when you can have our Men\'s Grey Oversized Pyjamas? Style it with tshirt and sneakers and let loose for the ultimate lounging experience.', 0, 0, 9),
(36, 12, 'ShopSavvy X Naruto', 699, 'static/upload/printed-pyjamas_naruto.png', 'Black Naruto All Over Printed Pyjamas', 0, 0, 9),
(37, 12, 'Blue Baggy Straight Fit J', 1499, 'static/upload/blue-baggy-straight-fit_jeans.png', 'The breathable denim fabric ensures a soft feel, keeping you comfortable whether you\'re out and about or taking it easy.', 0, 0, 28),
(38, 12, 'ShopSavvy X Marvel', 399, 'static/upload/black-iron-man.png', 'Black Iron Man of War', 0, 0, 15);

-- --------------------------------------------------------

--
-- Table structure for table `manage_subcat`
--

CREATE TABLE `manage_subcat` (
  `subcat_id` int(11) NOT NULL,
  `cat_id` int(11) NOT NULL,
  `supp_id` int(11) NOT NULL,
  `subcat_name` varchar(250) NOT NULL,
  `img` varchar(500) NOT NULL,
  `supp_desc` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `manage_subcat`
--

INSERT INTO `manage_subcat` (`subcat_id`, `cat_id`, `supp_id`, `subcat_name`, `img`, `supp_desc`) VALUES
(5, 2, 0, 'Shirt', 'static/upload/shirt.jpg', 'cotton shirt'),
(6, 12, 0, 'Oversized T-shirt', 'static/upload/oversized_t-shirt.png', 'dndjvn jasmc, ca haajfnioemfcm '),
(7, 12, 0, 'Joggers', 'static/upload/Joggers.png', ' ssckw akmam c jwenjc'),
(8, 12, 0, 'Shirts', 'static/upload/shirt.png', ' cma f32fwkqksa ,c  mcmc'),
(9, 12, 0, 'Pyjamas', 'static/upload/Pyjamas.png', 'jwqcnksa askvc am'),
(10, 12, 0, 'Shorts', 'static/upload/Shorts.png', ' dsknewv  ,sz  '),
(11, 12, 0, 'Classic Fit T-shirts', 'static/upload/Classic_fit_T-shirt.png', ' daejwv kc  kwqcm,sa'),
(12, 12, 0, 'Cargos', 'static/upload/Cargos.png', 'necm,s   ṣṣ mvdkoewldc z '),
(13, 12, 0, 'Pants', 'static/upload/Pants.png', 'ba cvc3jmew,s caxzm,'),
(14, 12, 0, 'Full Sleeve T-shirts', 'static/upload/Full_Sleeve_T-shirts.png', 'qwjh31ijwqm z cs x nmm'),
(15, 12, 0, 'Vests', 'static/upload/Vests.png', 'sando'),
(23, 14, 0, 'Swimwear', 'static/upload/swimwear.jpg', 'ShopSavvy Unisex Swim Set is designed for '),
(25, 13, 0, 'Oversized T-shirt', 'static/upload/OVERSIZED-T-SHIRTS.jpg', 'nmsc qwjnvckmas,'),
(26, 13, 0, 'Cragos', 'static/upload/CargosWomen.png', ' dswl3iecnm omc mm'),
(27, 14, 0, 'Jumpsuit', 'static/upload/jumpsuit.png', 'comfy jumpsuit '),
(28, 12, 0, 'Jeans', 'static/upload/Jeans.png', 'type of trousers made from denim or dungaree cloth');

-- --------------------------------------------------------

--
-- Table structure for table `order_details`
--

CREATE TABLE `order_details` (
  `detail_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `u_email` varchar(50) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `address` varchar(200) NOT NULL,
  `country` varchar(50) NOT NULL,
  `state` varchar(50) NOT NULL,
  `city` varchar(50) NOT NULL,
  `pin_code` int(11) NOT NULL,
  `pymnt_method` varchar(50) NOT NULL,
  `disp_id` int(11) NOT NULL,
  `status` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `order_details`
--

INSERT INTO `order_details` (`detail_id`, `user_id`, `name`, `u_email`, `mobile`, `address`, `country`, `state`, `city`, `pin_code`, `pymnt_method`, `disp_id`, `status`) VALUES
(1, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road........', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'cash', 0, 0),
(3, 11, 'hemani vadgama', 'vadgamahemangi08@gmail.com', 7862812091, 'Opp jubliee baug, prabhat studios lane, near sangam shoes raopura road.', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'online', 0, 0),
(5, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road........', 'INDIA', '', '', 0, 'cash', 0, 0),
(6, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road........', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'online', 0, 0),
(7, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road........', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'online', 0, 0),
(8, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road........', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'cash', 0, 0),
(9, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road........', 'INDIA', '', '', 0, 'online', 0, 0),
(10, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road........', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'cash', 0, 0),
(11, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road........', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'online', 0, 0),
(12, 10, 'Kriya Patel', 'kriyapatel63@gmail.com', 8160843810, 'Tower char rasta raopura road vadodara ', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'cash', 0, 0),
(13, 10, 'Kriya Patel', 'kriyapatel63@gmail.com', 8160843810, 'Tower char rasta raopura road vadodara ', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'cash', 0, 0),
(14, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road........', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'cash', 12, 1),
(15, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road........', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'cash', 0, 0),
(16, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road........', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'cash', 0, 0),
(17, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road........', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'cash', 0, 0),
(18, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road........', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'cash', 0, 0),
(19, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road........', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'cash', 0, 0),
(20, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road........', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'cash', 0, 0),
(21, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road........', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'cash', 0, 0),
(22, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road........', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'cash', 0, 0),
(23, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road........', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'cash', 0, 0),
(24, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road........', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'cash', 0, 0),
(25, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road........', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'cash', 0, 0),
(26, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road........', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'cash', 0, 0),
(27, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road........', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'cash', 0, 0),
(28, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road........', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'cash', 0, 0),
(29, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road........', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'cash', 0, 0),
(31, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road........', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'cash', 0, 0),
(32, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road........', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'cash', 0, 0),
(33, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road........', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'cash', 0, 0),
(34, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road........', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'cash', 0, 0),
(35, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road........', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'cash', 0, 0),
(36, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road........', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'cash', 0, 0),
(37, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road........', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'cash', 0, 0),
(38, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road........', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'cash', 0, 0),
(39, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road........', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'cash', 0, 0),
(40, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road........', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'cash', 0, 0),
(41, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road........', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'cash', 0, 0),
(42, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road........', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'cash', 0, 0),
(43, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road........', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'cash', 0, 0),
(44, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road........', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'cash', 0, 0),
(45, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road........', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'cash', 0, 0),
(46, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road........', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'cash', 0, 0),
(47, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road........', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'cash', 0, 0),
(48, 12, 'meet patel', 'meetbgt4243@gmail.com', 9377077617, 'gotri road', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'online', 15, 1),
(50, 13, 'Parth Patel', 'patelparth7719@gmail.com', 9734527733, 'manjalpur vadodara ', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'online', 0, 0),
(51, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'online', 0, 0),
(52, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'online', 0, 0),
(53, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'online', 0, 0),
(54, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'online', 0, 0),
(55, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'online', 0, 0),
(56, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'online', 0, 0),
(57, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'cash', 0, 0),
(58, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road', 'INDIA', '', '', 0, 'cash', 0, 0),
(59, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'cash', 0, 0),
(60, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'cash', 0, 0),
(61, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'online', 0, 0),
(62, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Opp jubliee garden prabhat studios lane near sangam shoes rao pura road', 'INDIA', '', '', 0, 'online', 0, 0),
(63, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Raopura road vadodara', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'cash', 0, 0),
(64, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Raopura road vadodara', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'online', 0, 0),
(65, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Raopura road vadodara', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'online', 0, 0),
(66, 1, 'Tisha Jinger', 'tishajinger0310@gmail.com', 6353138899, 'Raopura road vadodara', 'INDIA', 'Gujarat', 'Vadodara', 390001, 'cash', 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `order_tbl`
--

CREATE TABLE `order_tbl` (
  `order_id` int(11) NOT NULL,
  `detail_id` int(11) NOT NULL,
  `order_num` varchar(50) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `prdct_id` int(11) NOT NULL,
  `qty` int(200) NOT NULL,
  `date` datetime NOT NULL DEFAULT current_timestamp(),
  `pymnt_method` varchar(50) NOT NULL,
  `total_amt` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `order_tbl`
--

INSERT INTO `order_tbl` (`order_id`, `detail_id`, `order_num`, `user_id`, `prdct_id`, `qty`, `date`, `pymnt_method`, `total_amt`) VALUES
(2, 0, '816284', 11, 19, 1, '2025-04-10 12:43:47', 'Online', 824.82),
(3, 0, '159495', 11, 19, 1, '2025-04-10 12:47:07', 'Online', 2062.64),
(4, 0, '159495', 11, 18, 1, '2025-04-10 12:47:07', 'Online', 2062.64),
(30, 0, '392943', 10, 19, 1, '2025-04-11 13:53:09', 'cash', 1488.00),
(31, 0, '870345', 10, 26, 1, '2025-04-11 13:53:09', 'cash', 2976.00),
(32, 13, '445346', 10, 19, 1, '2025-04-11 13:59:15', 'cash', 699.00),
(39, 0, '636541', 12, 31, 1, '2025-04-17 11:39:42', 'Online', 824.82),
(40, 0, '610051', 12, 29, 1, '2025-04-17 11:45:17', 'Online', 942.82),
(41, 48, '479834', 12, 29, 1, '2025-04-17 11:45:31', 'online', 799.00),
(42, 49, '338950', 11, 19, 1, '2025-04-17 12:03:30', 'cash', 2198.00),
(43, 49, '204262', 11, 18, 1, '2025-04-17 12:03:30', 'cash', 4396.00),
(44, 49, '918828', 11, 31, 1, '2025-04-17 12:03:30', 'cash', 6594.00),
(45, 49, '111721', 11, 30, 1, '2025-04-17 12:03:30', 'cash', 8792.00),
(46, 0, '976900', 13, 31, 1, '2025-04-17 12:15:18', 'Online', 1767.64),
(47, 0, '976900', 13, 29, 1, '2025-04-17 12:15:18', 'Online', 1767.64),
(48, 50, '742289', 13, 31, 1, '2025-04-17 12:15:21', 'online', 1498.00),
(49, 50, '504614', 13, 29, 1, '2025-04-17 12:15:21', 'online', 2996.00),
(54, 0, '273345', 1, 29, 2, '2025-04-19 04:10:16', 'Online', 2411.85),
(55, 0, '273345', 1, 31, 1, '2025-04-19 04:10:16', 'Online', 2411.85),
(56, 0, '316922', 1, 29, 1, '2025-04-19 04:15:20', 'Online', 838.95),
(57, 65, 'ORD98319', 1, 29, 1, '2025-04-19 00:00:00', '', 799.00),
(58, 66, 'ORD10042', 1, 34, 2, '2025-04-19 00:00:00', '', 1398.00);

-- --------------------------------------------------------

--
-- Table structure for table `supplier_reg`
--

CREATE TABLE `supplier_reg` (
  `supp_id` int(11) NOT NULL,
  `supp_name` varchar(60) NOT NULL,
  `supp_bussName` varchar(70) NOT NULL,
  `address` text NOT NULL,
  `email_id` varchar(55) NOT NULL,
  `pwd` varchar(30) NOT NULL,
  `profile_img` text NOT NULL,
  `contact_no` int(10) NOT NULL,
  `s_status` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `supplier_reg`
--

INSERT INTO `supplier_reg` (`supp_id`, `supp_name`, `supp_bussName`, `address`, `email_id`, `pwd`, `profile_img`, `contact_no`, `s_status`) VALUES
(8, 'Kavya sharma', 'Arya Creation', 'Raj Nagar Society, Vadodara, Gujarat 390020', 'kavya29@gmail.com', 'Creation2901', 'static/upload/WIN_20220724_20_52_55_Pro.jpg', 2147483647, 0),
(9, 'Parthvi Jingar', 'sherlock trendy', '3, Siddarth Complex, Vadodara, Gujarat 390007', 'parthvijingar1999@gmail.com', 'RaviP9998', 'static/upload/OMG_1084.JPG', 2147483647, 0);

-- --------------------------------------------------------

--
-- Table structure for table `user_reg`
--

CREATE TABLE `user_reg` (
  `user_id` int(11) NOT NULL,
  `u_email` varchar(100) NOT NULL,
  `name` varchar(20) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `gender` varchar(50) NOT NULL,
  `dob` date NOT NULL,
  `password` varchar(50) NOT NULL,
  `address` varchar(500) NOT NULL,
  `status` tinyint(1) NOT NULL,
  `verified` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_reg`
--

INSERT INTO `user_reg` (`user_id`, `u_email`, `name`, `mobile`, `gender`, `dob`, `password`, `address`, `status`, `verified`) VALUES
(1, 'tishajinger0310@gmail.com', 'Tisha Jinger', 6353138899, 'female', '2025-01-29', 'Tish@2002', 'Raopura road vadodara', 0, 0),
(10, 'kriyapatel63@gmail.com', 'Kriya Patel', 8160843810, 'Female', '2002-10-03', 'Kriy@63p@te!', 'Tower char rasta raopura road vadodara ', 0, 0),
(11, 'vadgamahemangi08@gmail.com', 'hemani vadgama', 7862812091, 'Female', '2002-07-08', 'Hem@ngi8890', 'Chaani road vadodara', 0, 0),
(12, 'meetbgt4243@gmail.com', 'meet patel', 9377077617, 'Male', '2004-05-27', 'Il143@123.', 'gotri road', 1, 0),
(13, 'patelparth7719@gmail.com', 'Parth Patel', 9734527733, 'Male', '2002-02-28', 'P@ppd!42490', 'manjalpur vadodara ', 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `wishlist`
--

CREATE TABLE `wishlist` (
  `wishlist_id` int(11) NOT NULL,
  `prdct_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `qty` int(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `wishlist`
--

INSERT INTO `wishlist` (`wishlist_id`, `prdct_id`, `user_id`, `qty`) VALUES
(1, 12, 1, 1),
(2, 19, 1, 1),
(12, 30, 10, 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `add_to_bag`
--
ALTER TABLE `add_to_bag`
  ADD PRIMARY KEY (`bag_id`);

--
-- Indexes for table `add_to_cart`
--
ALTER TABLE `add_to_cart`
  ADD PRIMARY KEY (`cart_id`);

--
-- Indexes for table `admin_login`
--
ALTER TABLE `admin_login`
  ADD PRIMARY KEY (`Admin_id`);

--
-- Indexes for table `customization`
--
ALTER TABLE `customization`
  ADD PRIMARY KEY (`cust_id`);

--
-- Indexes for table `feedback`
--
ALTER TABLE `feedback`
  ADD PRIMARY KEY (`user_id`);

--
-- Indexes for table `manage_cat`
--
ALTER TABLE `manage_cat`
  ADD PRIMARY KEY (`cat_id`);

--
-- Indexes for table `manage_disp`
--
ALTER TABLE `manage_disp`
  ADD PRIMARY KEY (`disp_id`);

--
-- Indexes for table `manage_prdct`
--
ALTER TABLE `manage_prdct`
  ADD PRIMARY KEY (`prdct_id`);

--
-- Indexes for table `manage_subcat`
--
ALTER TABLE `manage_subcat`
  ADD PRIMARY KEY (`subcat_id`);

--
-- Indexes for table `order_details`
--
ALTER TABLE `order_details`
  ADD PRIMARY KEY (`detail_id`);

--
-- Indexes for table `order_tbl`
--
ALTER TABLE `order_tbl`
  ADD PRIMARY KEY (`order_id`);

--
-- Indexes for table `supplier_reg`
--
ALTER TABLE `supplier_reg`
  ADD PRIMARY KEY (`supp_id`);

--
-- Indexes for table `user_reg`
--
ALTER TABLE `user_reg`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `u_email` (`u_email`);

--
-- Indexes for table `wishlist`
--
ALTER TABLE `wishlist`
  ADD PRIMARY KEY (`wishlist_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `add_to_bag`
--
ALTER TABLE `add_to_bag`
  MODIFY `bag_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `add_to_cart`
--
ALTER TABLE `add_to_cart`
  MODIFY `cart_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=46;

--
-- AUTO_INCREMENT for table `admin_login`
--
ALTER TABLE `admin_login`
  MODIFY `Admin_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `customization`
--
ALTER TABLE `customization`
  MODIFY `cust_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `feedback`
--
ALTER TABLE `feedback`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `manage_cat`
--
ALTER TABLE `manage_cat`
  MODIFY `cat_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `manage_disp`
--
ALTER TABLE `manage_disp`
  MODIFY `disp_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `manage_prdct`
--
ALTER TABLE `manage_prdct`
  MODIFY `prdct_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=39;

--
-- AUTO_INCREMENT for table `manage_subcat`
--
ALTER TABLE `manage_subcat`
  MODIFY `subcat_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT for table `order_details`
--
ALTER TABLE `order_details`
  MODIFY `detail_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=67;

--
-- AUTO_INCREMENT for table `order_tbl`
--
ALTER TABLE `order_tbl`
  MODIFY `order_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=59;

--
-- AUTO_INCREMENT for table `supplier_reg`
--
ALTER TABLE `supplier_reg`
  MODIFY `supp_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `user_reg`
--
ALTER TABLE `user_reg`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `wishlist`
--
ALTER TABLE `wishlist`
  MODIFY `wishlist_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
